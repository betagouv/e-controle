<template>
  <div>
    <div>TODO REMOVE DEBUG OUTPUT</div>
    <div>{{ currentQuestionnaire }}</div>
    <swap-editor-button v-if="controlHasMultipleInspectors"
                        :control-id="controlId"
                        @save-draft="saveDraftBeforeEditorSwap">
    </swap-editor-button>
    <div class="page-header">
      <div class="page-title flex-wrap">
        <i class="fe fe-list mr-2"></i>
        <span v-if="currentQuestionnaire.is_draft || currentQuestionnaire.id === undefined"
              class="tag tag-azure big-tag round-tag font-italic mr-2">
          Brouillon
        </span>
        <span>Rédaction du Questionnaire n°{{ questionnaireNumbering }}</span>
        <span v-if="currentQuestionnaire.title" class="ml-1"> - {{ currentQuestionnaire.title }}</span>
      </div>
    </div>
    <div v-if="hasErrors" class="alert alert-danger" id="questionnaire-create-error">
      {{ errorMessage }}
    </div>

    <questionnaire-metadata-create
            id="questionnaire-metadata-create"
            ref="createMetadataChild"
            :questionnaire-numbering="questionnaireNumbering"
            v-on:next="next"
            v-on:save-draft="saveDraft"
            v-show="state === STATES.START">
    </questionnaire-metadata-create>
    <questionnaire-body-create
            ref="createBodyChild"
            v-on:next="next"
            v-on:save-draft="saveDraft"
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
import { loadStatuses } from '../store'
import moment from 'moment'
import { mapFields } from 'vuex-map-fields'
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
    controlHasMultipleInspectors: Boolean,
    questionnaireId: Number,
    questionnaireNumbering: Number,
  },
  data() {
    return {
      errorMessage: '',
      errors: [],
      hasErrors: false,
      STATES: STATES,
      state: '',
      message: '',
    }
  },
  computed: {
    ...mapFields([
      'controls',
      'controlsLoadStatus',
      'currentQuestionnaire',
    ]),
  },
  watch: {
    controlsLoadStatus(newValue, oldValue) {
      if (newValue === loadStatuses.SUCCESS) {
        if (typeof this.questionnaireId === 'undefined') {
          const newQuestionnaire = {
            control: this.controlId,
            description: QuestionnaireMetadataCreate.DESCRIPTION_DEFAULT,
          }
          console.debug('currentQuestionnaire is new', newQuestionnaire)
          this.currentQuestionnaire = newQuestionnaire
          this.emitQuestionnaireUpdated()
          this.moveToState(STATES.START)
          return
        }
        const currentQuestionnaire = this.findCurrentQuestionnaire(this.controls, this.questionnaireId)
        // Todo : what if no questionnaire?
        // Todo : What if not a draft?
        console.debug('currentQuestionnaire', currentQuestionnaire)
        this.currentQuestionnaire = currentQuestionnaire
        this.emitQuestionnaireUpdated()
        this.moveToState(STATES.START)
      }
      // todo do something on loadStatuses.ERROR
    },
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
  },
  methods: {
    findCurrentQuestionnaire: function(controls, questionnaireId) {
      for (let i = 0; i < controls.length; i++) {
        const control = controls[i]
        const foundQuestionnaires =
          control.questionnaires.filter(questionnaire => questionnaire.id === questionnaireId)
        if (foundQuestionnaires.length > 0) {
          return foundQuestionnaires[0]
        }
      }
    },
    emitQuestionnaireUpdated: function() {
      this.$emit('questionnaire-updated', this.questionnaire)
    },
    moveToState: function(newState) {
      this.clearErrors()
      this.state = newState
    },
    next: function() {
      console.debug('Navigation "next" from', this.state)
      this.saveDraft()
      if (this.state === STATES.START) {
        this.moveToState(STATES.CREATING_BODY)
        return
      }
      if (this.state === STATES.CREATING_BODY) {
        this.moveToState(STATES.PREVIEW)
        return
      }
      console.error('Trying to go to "next", from state', this.state)
    },
    back: function(clickedStep) {
      console.debug('Navigation "back" from', this.state, 'going to step', clickedStep)
      if (this.state === STATES.CREATING_BODY) {
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
        if (this.currentQuestionnaire.end_date) {
          this.currentQuestionnaire.end_date = moment(String(this.currentQuestionnaire.end_date)).format('YYYY-MM-DD')
        } else {
          delete this.currentQuestionnaire.end_date // remove empty strings, it throws date format error.
        }
      }
      const getCreateMethod = () => axios.post.bind(this, backend.questionnaire())
      const getUpdateMethod =
          (questionnaireId) => axios.put.bind(this, backend.questionnaire(questionnaireId))

      this.clearErrors()
      cleanPreSave()

      let saveMethod
      if (this.currentQuestionnaire.id !== undefined) {
        saveMethod = getUpdateMethod(this.currentQuestionnaire.id)
      } else {
        saveMethod = getCreateMethod()
      }
      return saveMethod(this.currentQuestionnaire)
    },
    saveDraftBeforeEditorSwap() {
      console.debug('save draft before editor swap')
      const validateForm = () => {
        if (this.state === STATES.PREVIEW) {
          return true
        }
        if (this.state === STATES.START) {
          return this.$refs.createMetadataChild.validateForm()
        }
        if (this.state === STATES.CREATING_BODY) {
          return this.$refs.createBodyChild.validateForm()
        }
      }

      if (!validateForm()) {
        return
      }
      this.saveDraft()
        .then(savedQuestionnaire => {
          this.$emit('show-swap-editor-modal', savedQuestionnaire.id)
        })
    },
    saveDraft() {
      this.currentQuestionnaire.is_draft = true
      return this._doSave()
        .then((response) => {
          console.log('Successful draft save.')
          this.currentQuestionnaire = response.data
          this.emitQuestionnaireUpdated()

          const timeString = moment(new Date()).format('HH:mm:ss')
          this.message = 'Votre dernière sauvegarde a eu lieu à ' + timeString + '.'
          return response.data
        })
        .catch((error) => {
          console.error('Error in draft save :', error)
          const errorToDisplay = (error.response && error.response.data) ? error.response.data : error
          this.displayErrors('Erreur lors de la sauvegarde du brouillon.', errorToDisplay)
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
