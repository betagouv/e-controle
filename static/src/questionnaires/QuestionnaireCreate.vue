<template>
<div>
  <div class="mx-3">
    <breadcrumbs v-if="state !== STATES.LOADING" :control="currentControl"></breadcrumbs>
    <swap-editor-button v-if="state !== STATES.LOADING && controlHasMultipleInspectors"
                        :control-id="controlId"
                        @save-draft="saveDraftAndSwapEditor">
    </swap-editor-button>
    <div class="page-header">
      <div class="page-title flex-wrap">
        <i class="fe fe-list mr-2"></i>
        <span v-if="currentQuestionnaire.is_draft || currentQuestionnaire.id === undefined"
              class="tag tag-azure big-tag round-tag font-italic mr-2">
          Brouillon
        </span>
        <span>
          Rédaction du Questionnaire n°{{ questionnaireNumbering }}
        </span>
        <span v-if="currentQuestionnaire.title" class="ml-1">
          - {{ currentQuestionnaire.title }}
        </span>
      </div>
    </div>
    <div v-if="hasErrors" class="alert alert-danger" id="questionnaire-create-error">
      {{ errorMessage }}
    </div>

    <div v-if="state === STATES.LOADING"
         class="card mt-9">
      <div class="card-body flex-column align-items-center">
        <div class="loader"></div>
        <div class="mt-4"> En chargement ... </div>
      </div>
    </div>
    <div v-else
         id="page-middle">
      <wizard id="wizard"
              :active-step-number="this.state"
              :step-titles="['Renseigner l\'introduction',
                            'Ajouter des questions',
                            'Aperçu avant publication']"
              @next="next"
              @previous="back">
      </wizard>

      <questionnaire-metadata-create
              id="questionnaire-metadata-create"
              ref="questionnaireMetadataCreate"
              :questionnaire-numbering="questionnaireNumbering"
              v-show="state === STATES.START">
      </questionnaire-metadata-create>
      <questionnaire-body-create
              id="questionnaire-body-create"
              ref="questionnaireBodyCreate"
              v-show="state === STATES.CREATING_BODY">
      </questionnaire-body-create>
      <questionnaire-preview
              id="questionnaire-preview"
              v-show="state === STATES.PREVIEW">
      </questionnaire-preview>
    </div>
  </div>

  <!-- Note : use v-show and not v-if for the bottom-bar, because the element needs to be in the DOM
  from the start for the IE sticky-bottom to work. -->
  <div id="bottom-bar"
       v-show="state !== STATES.LOADING"
       class="flex-column bg-white sticky-bottom border-top p-4">
    <div id="button-bar" class="flex-row justify-content-between">
      <button id="go-home-button"
              type="button"
              class="btn btn-secondary"
              @click="saveDraftAndGoHome"
      >
        <i class="fa fa-chevron-left mr-2"></i>
        Retour
      </button>
      <div>
        <button v-if="state !== STATES.START"
                id="back-button"
                @click="back"
                class="btn btn-secondary">
          <i class="fa fa-chevron-left mr-2"></i>
          Etape {{ state - 1 }}
        </button>
        <button v-if="state === STATES.CREATING_BODY"
                id="move-themes-button"
                role="button"
                type="button"
                class="btn btn-secondary"
                @click="saveAndShowMoveThemesModal"
                title="Réorganiser les thèmes">
          <i class="fa fa-exchange-alt fa-rotate-90"></i>
          Réorganiser les thèmes
        </button>
        <button @click="validateFormAndSaveDraft"
                class="btn btn-primary">
          <i class="fe fe-save"></i>
          Enregistrer
        </button>
        <button v-if="state !== STATES.PREVIEW"
                id="next-button"
                @click="next"
                class="btn btn-secondary">
          Etape {{ state + 1 }}
          <i class="fa fa-chevron-right ml-2"></i>
        </button>
        <button v-if="state === STATES.PREVIEW"
                id="publishButton"
                ref="publishButton"
                @click="startPublishFlow()"
                class="btn btn-primary ml-5"
                title="Publier le questionnaire à l'organisme interrogé">
          <i class="fa fa-rocket mr-1"></i>
          Publier
        </button>
      </div>
    </div>
    <div class="flex-row justify-content-end mt-2">
      <div class="text-muted" style="min-height: 1.5rem;">
        {{ saveMessage }}
      </div>
    </div>
  </div>

  <publish-flow ref="publishFlow"
                :publishFunction="publish"
                :controlId="currentQuestionnaire.control">
  </publish-flow>

</div>
</template>

<script>
import axios from 'axios'
import backend from '../utils/backend'
import { nowTimeString, toBackendFormat } from '../utils/DateFormat'
import Breadcrumbs from '../utils/Breadcrumbs'
import { loadStatuses } from '../store'
import { mapFields } from 'vuex-map-fields'
import PublishFlow from './PublishFlow'
import QuestionnaireBodyCreate from './QuestionnaireBodyCreate'
import QuestionnaireMetadataCreate from './QuestionnaireMetadataCreate'
import QuestionnairePreview from './QuestionnairePreview'
import StickyBottomMixin from '../utils/StickyBottomMixin'
import SwapEditorButton from '../editors/SwapEditorButton'
import Vue from 'vue'
import Wizard from '../utils/Wizard'

// State machine
const STATES = {
  LOADING: 0,
  START: 1,
  CREATING_BODY: 2,
  PREVIEW: 3,
}

axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'

export default Vue.extend({
  props: {
    controlId: Number,
    controlHasMultipleInspectors: Boolean,
    questionnaireId: Number,
    questionnaireNumbering: Number,
    // Pass window dependency for testing
    window: {
      default: () => window,
    },
  },
  data() {
    return {
      errorMessage: '',
      errors: [],
      hasErrors: false,
      STATES: STATES,
      state: STATES.LOADING,
      saveMessage: '',
    }
  },
  computed: {
    ...mapFields([
      'controls',
      'controlsLoadStatus',
      'currentQuestionnaire',
    ]),
    currentControl() {
      if (!this.currentQuestionnaire || !this.currentQuestionnaire.control) {
        return null
      }
      return this.controls.find(control => control.id === this.currentQuestionnaire.control)
    },
  },
  watch: {
    // Watch change of loadStatus coming from the store, to know when the data is ready.
    controlsLoadStatus(newValue, oldValue) {
      const loadNewQuestionnaire = () => {
        console.debug('loadNewQuestionnaire')
        const newQuestionnaire = {
          control: this.controlId,
          description: QuestionnaireMetadataCreate.DESCRIPTION_DEFAULT,
          title: '',
          themes: [],
        }
        console.debug('currentQuestionnaire is new', newQuestionnaire)
        this.currentQuestionnaire = newQuestionnaire
        this.emitQuestionnaireUpdated()
        this.moveToState(STATES.START)
        return
      }

      const loadExistingQuestionnaire = () => {
        console.debug('loadExistingQuestionnaire')
        const currentQuestionnaire =
          this.findCurrentQuestionnaire(this.controls, this.questionnaireId)
        console.debug('currentQuestionnaire', currentQuestionnaire)
        if (!currentQuestionnaire) {
          const errorMessage = 'Le questionnaire ' + this.questionnaireId + ' n\'a pas été trouvé.'
          this.displayErrors(errorMessage)
          throw new Error('Questionnaire ' + this.questionnaireId + ' not found')
        }
        if (!currentQuestionnaire.is_draft) {
          const errorMessage = 'Le questionnaire ' + this.questionnaireId +
                ' n\'est pas un brouillon. Vous ne pouvez pas le modifier.'
          this.displayErrors(errorMessage)
          throw new Error(
            'Questionnaire ' + this.questionnaireId + ' is not a draft, you cannot edit it')
        }
        this.currentQuestionnaire = currentQuestionnaire
        this.emitQuestionnaireUpdated()
        this.moveToState(STATES.START)
      }

      if (newValue === loadStatuses.ERROR) {
        const errorMessage =
          'Erreur lors du chargement des données. Le questionnaire ne peut être affiché.'
        this.displayErrors(errorMessage)
        throw new Error('Store status is ERROR. Not loading questionnaire.')
      }
      if (newValue === loadStatuses.SUCCESS) {
        if (typeof this.questionnaireId === 'undefined') {
          loadNewQuestionnaire()
          return
        }
        loadExistingQuestionnaire()
      }
    },
  },
  components: {
    Breadcrumbs,
    PublishFlow,
    QuestionnaireBodyCreate,
    QuestionnaireMetadataCreate,
    QuestionnairePreview,
    SwapEditorButton,
    Wizard,
  },
  mixins: [
    StickyBottomMixin,
  ],
  mounted() {
    this.stickyBottom_makeStickyBottom('bottom-bar', 140, 103, 44)

    console.debug('questionnaireId', this.questionnaireId)
    console.debug('controlId', this.controlId)
    if (this.controlId === undefined && this.questionnaireId === undefined) {
      throw Error('QuestionnaireCreate needs a controlId or a questionnaireId')
    }
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
      this.$emit('questionnaire-updated', this.currentQuestionnaire)
    },
    moveToState: function(newState) {
      this.clearErrors()
      this.state = newState
    },
    next: function() {
      console.debug('Navigation "next" from', this.state)
      if (this.state === STATES.START) {
        if (!this.$refs.questionnaireMetadataCreate.validateForm()) {
          return
        }
        this.saveDraft().then(() => {
          // If there are no themes, add an empty theme and question, to prompt the user to add
          // more.
          if (this.currentQuestionnaire.themes.length === 0) {
            this.currentQuestionnaire.themes.push({ questions: [{}] })
          }
          this.moveToState(STATES.CREATING_BODY)
          return
        })
        return
      }
      if (this.state === STATES.CREATING_BODY) {
        if (!this.$refs.questionnaireBodyCreate.validateForm()) {
          return
        }
        this.saveDraft()
        this.moveToState(STATES.PREVIEW)
        return
      }
      console.error('Trying to go to "next", from state', this.state)
    },
    back: function(clickedStep) {
      console.debug('Navigation "back" from', this.state, 'going to step', clickedStep)
      if (this.state === STATES.CREATING_BODY) {
        if (!this.$refs.questionnaireBodyCreate.validateForm()) {
          return
        }
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
        // no step specified so, go to previous step by default
        this.moveToState(STATES.CREATING_BODY)
        return
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
    clearSaveMessage() {
      this.saveMessage = ''
    },
    _doSave() {
      const cleanPreSave = () => {
        if (this.currentQuestionnaire.end_date) {
          this.currentQuestionnaire.end_date = toBackendFormat(this.currentQuestionnaire.end_date)
        } else {
          // remove empty strings, it throws date format error.
          delete this.currentQuestionnaire.end_date
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
    validateCurrentForm() {
      if (this.state === STATES.PREVIEW) {
        return true
      }
      if (this.state === STATES.START) {
        return this.$refs.questionnaireMetadataCreate.validateForm()
      }
      if (this.state === STATES.CREATING_BODY) {
        return this.$refs.questionnaireBodyCreate.validateForm()
      }
    },
    saveDraftAndSwapEditor() {
      console.debug('save draft before editor swap')
      if (!this.validateCurrentForm()) {
        return
      }
      this.saveDraft()
        .then(savedQuestionnaire => {
          this.$emit('show-swap-editor-modal', savedQuestionnaire.id)
        })
    },
    validateFormAndSaveDraft() {
      if (!this.validateCurrentForm()) {
        return
      }
      this.saveDraft()
    },
    saveDraft() {
      this.currentQuestionnaire.is_draft = true
      return this._doSave()
        .then((response) => {
          console.log('Successful draft save.')
          this.currentQuestionnaire = response.data
          this.emitQuestionnaireUpdated()

          this.saveMessage = 'Votre dernière sauvegarde a eu lieu à ' + nowTimeString() + '.'
          return response.data
        })
        .catch((error) => {
          console.error('Error in draft save :', error)
          const errorToDisplay =
            (error.response && error.response.data) ? error.response.data : error
          this.displayErrors('Erreur lors de la sauvegarde du brouillon.', errorToDisplay)
        })
    },
    startPublishFlow() {
      this.$refs.publishFlow.start()
    },
    publish() {
      this.currentQuestionnaire.is_draft = false
      return this._doSave()
    },
    saveDraftAndGoHome(event) {
      if (!this.validateCurrentForm()) {
        return
      }
      // Display a "loading" spinner on clicked button, while the user is redirected, so that they
      // know their click has been registered.
      $(event.target).addClass('btn-loading')
      this.saveDraft()
        .then(() => {
          // Whether or not save succeeds, navigate to home
          this.goHome()
        })
    },
    goHome() {
      this.window.location.href = backend['control-detail'](this.currentQuestionnaire.control)
    },
    saveAndShowMoveThemesModal() {
      if (!this.validateCurrentForm()) {
        return
      }
      $('#move-themes-button').addClass('btn-loading')
      this.saveDraft()
        .then(() => {
          $('#move-themes-button').removeClass('btn-loading')
          // Only display moveThemesModal if the user is still on the same page.
          if (this.state === STATES.CREATING_BODY) {
            $(this.$refs.questionnaireBodyCreate.$refs.moveThemesModal.$el).modal('show')
          }
        })
    },
  },
})
</script>

<style scoped>
  #bottom-bar {
    margin-left: -2rem;
    margin-right: -0.75rem;
  }
</style>
