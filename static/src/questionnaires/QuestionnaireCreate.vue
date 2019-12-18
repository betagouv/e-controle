<template>
  <div>
    <swap-editor-button :control-id='controlId'
                        :questionnaire-id='questionnaireId'>
    </swap-editor-button>

    <div class="page-header">
      <div class="page-title flex-wrap">
        <i class="fe fe-list mr-2"></i>
        <span v-if="questionnaire.is_draft || questionnaire.id === undefined"
              class="tag tag-azure big-tag round-tag font-italic mr-2">
          Brouillon
        </span>
        <span>Rédaction du Questionnaire n°{{ questionnaireNumbering }}</span>
        <span v-if="questionnaire.title" class="ml-1"> - {{ questionnaire.title }}</span>
      </div>
    </div>
    <div v-if="hasErrors" class="alert alert-danger" id="questionnaire-create-error">
      {{ errorMessage }}
    </div>

    <questionnaire-metadata-create
            id="questionnaire-metadata-create"
            ref="createMetadataChild"
            :questionnaire-numbering="questionnaireNumbering"
            v-on:metadata-created="onMetadataCreated"
            v-on:save-draft="saveDraftFromMetadata"
            v-show="state === STATES.START">
    </questionnaire-metadata-create>
    <questionnaire-body-create
            ref="createBodyChild"
            v-on:body-created="onBodyCreated"
            v-on:save-draft="saveDraftFromBody"
            v-on:back="back"
            v-show="state === STATES.CREATING_BODY">
    </questionnaire-body-create>
    <questionnaire-preview
            ref="previewChild"
            v-on:publish-questionnaire="publish()"
            v-on:save-draft="saveDraft"
            v-on:back="back"
            v-show="state === STATES.PREVIEW">
    </questionnaire-preview>
    <div class="card-header border-0"
         style="position:relative; bottom: 4.3rem;">
      <div class="card-options">
        {{ message }}
      </div>
    </div>
    <button type="button"
            class="btn btn-secondary"
            style="position:relative; bottom: 151px; left: 2em;"
            @click="goHome"
    >
      < Revenir à l'accueil
    </button>

    <empty-modal id="savingModal" ref="savingModal" no-close="true">
      <div class="d-flex flex-column align-items-center p-8">
        <div class="m-4">
          Questionnaire en cours de publication ...
        </div>
        <div class="loader m-4">
        </div>
      </div>
    </empty-modal>
    <empty-modal id="savedModal"
                 ref="savedModal"
                 no-close="true">
      <div class="modal-header border-bottom-0 flex-column align-items-center">
        <p>
          <i class="fe fe-check-circle fg-success big-icon"></i>
        </p>
        <h4 class="text-center">
          Bravo, votre questionnaire est publié!
        </h4>
      </div>
      <div class="modal-body text-center">
        <p>
          Si des réponses sont déposées par l'organisme interrogé, vous recevrez un email de notification dès le lendemain 8 heure.
        </p>
      </div>
      <div class="modal-footer border-top-0 d-flex justify-content-center">
        <button type="button" class="btn btn-primary"
                @click="goHome"
        >
          < Revenir à l'accueil
        </button>
      </div>
    </empty-modal>
  </div>
</template>

<script>
import axios from 'axios'
import backend from '../utils/backend'
import EmptyModal from '../utils/EmptyModal'
import EventBus from '../events'
import InfoBar from '../utils/InfoBar'
import moment from 'moment'
import QuestionnaireBodyCreate from './QuestionnaireBodyCreate'
import QuestionnaireMetadataCreate from './QuestionnaireMetadataCreate'
import QuestionnairePreview from './QuestionnairePreview'
import SwapEditorButton from '../editors/SwapEditorButton'
import Vue from 'vue'

// State machine
const STATES = {
  START: 'start',
  // Transition : metadata-created / back
  CREATING_BODY: 'creating_body',
  // Transition : body-created / back
  PREVIEW: 'preview',
}

const PUBLISH_TIME_MILLIS = 3000
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'

export default Vue.extend({
  props: {
    controlId: Number,
    questionnaireId: Number,
    questionnaireNumbering: Number,
  },
  data() {
    return {
      errorMessage: '',
      errors: [],
      hasErrors: false,
      STATES: STATES,
      questionnaire: {},
      state: '',
      message: '',
    }
  },
  components: {
    EmptyModal,
    QuestionnaireBodyCreate,
    QuestionnaireMetadataCreate,
    QuestionnairePreview,
    SwapEditorButton,
  },
  mounted() {
    console.debug('questionnaireId', this.questionnaireId)
    console.debug('controlId', this.controlId)
    if (!this.controlId && !this.questionnaireId) {
      throw Error('QuestionnaireCreate needs a controlId or a questionnaireId')
    }

    EventBus.$on('display-error', (errorMessage) => {
      this.displayErrors(errorMessage)
    })

    if (typeof this.controlId !== 'undefined') {
      this._loadQuestionnaireCreate()
      return
    }

    this._loadQuestionnaireUpdate()
  },
  methods: {
    _loadQuestionnaireCreate: function() {
      this.questionnaire.control = this.controlId
      this.questionnaire.description = QuestionnaireMetadataCreate.DESCRIPTION_DEFAULT
      this.emitQuestionnaireUpdated()
      console.debug('loaded new questionnaire', this.questionnaire)
      this.moveToState(STATES.START)
    },
    _loadQuestionnaireUpdate: function() {
      console.debug('Fetching draft questionnaire...')
      axios.get(backend.questionnaire(this.questionnaireId))
        .then(response => {
          console.debug('Got draft : ', response.data)
          if (response.data.is_draft !== undefined && !response.data.is_draft) {
            const errorMessage = 'Le questionnaire ' + response.data.id +
                ' n\'est pas un brouillon. Vous ne pouvez pas le modifier.'
            this.displayErrors(errorMessage)
            return
          }
          this.questionnaire = response.data
          this.emitQuestionnaireUpdated()
          this.moveToState(STATES.START)
        }).catch(error => {
          const errorToDisplay = (error.response && error.response.data) ? error.response.data : error
          this.displayErrors('Erreur lors du chargement du brouillon.', errorToDisplay)
        })
    },
    emitQuestionnaireUpdated: function() {
      this.$emit('questionnaire-updated', this.questionnaire)
    },
    moveToState: function(newState) {
      this.clearErrors()
      this.state = newState
    },
    onBodyCreated: function(body) {
      console.debug('QuestionnaireCreate got body', body)
      this._updateBody(body)
      this.saveDraft()
      this.moveToState(STATES.PREVIEW)
    },
    onMetadataCreated: function(metadata) {
      console.debug('got metadata', metadata)
      this._updateMetadata(metadata)
      this.saveDraft()
      this.moveToState(STATES.CREATING_BODY)
    },
    _updateBody(body) {
      this.questionnaire.themes = body
    },
    _updateMetadata: function(metadata) {
      for (const [key, value] of Object.entries(metadata)) {
        this.questionnaire[key] = value
      }
    },
    _updateQuestionnaire: function(questionnaire) {
      this.questionnaire.id = questionnaire.id
      const metadata = {
        description: questionnaire.description,
        end_date: questionnaire.end_date,
        title: questionnaire.title,
      }
      this._updateMetadata(metadata)
      this._updateBody(questionnaire.themes)
    },
    back: function(clickedStep, data) {
      console.debug('back', clickedStep, data)
      if (this.state === STATES.CREATING_BODY) {
        this._updateBody(data)
        this.saveDraft()
        this.moveToState(STATES.START)
        return
      }
      if (this.state === STATES.PREVIEW) {
        if (clickedStep === 1) {
          this.moveToState(STATES.START)
          return
        }
        if (clickedStep === 2) {
          this.moveToState(STATES.CREATING_BODY)
          return
        }
      }
      console.error('Trying to go back from state', this.state, 'with clickedStep', clickedStep)
    },
    displayErrors: function(errorMessage, errors) {
      this.hasErrors = true
      this.errors = errors
      if (errors) {
        this.errorMessage = errorMessage + ' Erreurs : ' + JSON.stringify(errors)
      } else {
        this.errorMessage = errorMessage
      }
      console.error(errorMessage)
    },
    clearErrors() {
      this.hasErrors = false
      this.errors = []
      this.errorMessage = ''
    },
    clearMessages() {
      this.message = ''
    },
    _doSave() {
      const cleanPreSave = () => {
        if (this.questionnaire.end_date) {
          this.questionnaire.end_date = moment(String(this.questionnaire.end_date)).format('YYYY-MM-DD')
        } else {
          delete this.questionnaire.end_date // remove empty strings, it throws date format error.
        }
      }
      const getCreateMethod = () => axios.post.bind(this, backend.questionnaire())
      const getUpdateMethod =
          (questionnaireId) => axios.put.bind(this, backend.questionnaire(questionnaireId))

      this.clearErrors()
      cleanPreSave()

      let saveMethod
      if (this.questionnaire.id !== undefined) {
        saveMethod = getUpdateMethod(this.questionnaire.id)
      } else {
        saveMethod = getCreateMethod()
      }
      return saveMethod(this.questionnaire)
    },
    saveDraftFromMetadata(data) {
      this._updateMetadata(data)
      this.saveDraft()
    },
    saveDraftFromBody(data) {
      this._updateBody(data)
      this.saveDraft()
    },
    saveDraft() {
      this.questionnaire.is_draft = true
      this._doSave()
        .then((response) => {
          this._updateQuestionnaire(response.data)
          this.emitQuestionnaireUpdated()

          const timeString = moment(new Date()).format('HH:mm:ss')
          this.message = 'Votre dernière sauvegarde a eu lieu à ' + timeString + '.'
        })
        .catch((error) => {
          console.error(error)
          this.displayErrors('Erreur lors de la sauvegarde du brouillon.', error.response.data)
        })
    },
    wait(timeMillis) {
      return new Promise((resolve) => {
        const id = setTimeout(() => {
          clearTimeout(id)
          resolve()
        }, timeMillis)
      })
    },
    publish() {
      $(this.$refs.savingModal.$el).modal('show')
      this.questionnaire.is_draft = false

      // Leave the "Saving..." modal for at least PUBLISH_TIME_MILLIS.
      // This is for the user to see the wait modal and be satisfied that the saving really happened.
      return Promise.all([this.wait(PUBLISH_TIME_MILLIS), this._doSave()])
        .then(() => {
          console.debug('Done publishing questionnaire.')
          $(this.$refs.savingModal.$el).modal('hide')
          $(this.$refs.savedModal.$el).modal('show')
        })
        .catch(error => {
          console.error('Error publishing questionnaire : ', error)
          $(this.$refs.savingModal.$el).modal('hide')
          // Emettre un event pour QuestionnairePreview, pour reafficher le modal
          this.$emit('publish-questionnaire-error', error)
        })
    },
    goHome(event) {
      // Display a "loading" spinner on clicked button, while the user is redirected, so that they know their click
      // has been registered.
      $(event.target).addClass('btn-loading')

      window.location.href = backend['control-detail'](this.questionnaire.control)
    },
  },
})
</script>

<style></style>
