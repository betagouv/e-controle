<template>
  <div>
    <div class="page-header">
      <div class="page-title">
        <span v-if="questionnaire.is_draft" class="tag tag-azure big-tag mr-2">Brouillon</span>
        <span>Rédaction du Questionnaire n°{{ questionnaireNumbering }}</span>
        <span v-if="questionnaire"> - {{ questionnaire.title }}</span>
      </div>
    </div>
    <button @click="saveNonDraft"
            class="btn btn-primary">
      des trucs
    </button>
    <div v-if="hasErrors" class="alert alert-danger">
      {{ errorMessage }}
    </div>
    <info-bar>
      Vous êtes le rédacteur de ce brouillon de questionnaire. Vos collègues de l'équipe de contrôle pourront le voir, mais pas le modifier.
    </info-bar>
    <questionnaire-metadata-create
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
            v-on:save-questionnaire="saveNonDraft"
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
    <a :href="home_url"
       class="btn btn-secondary"
       style="position:relative; bottom: 151px; left: 2em;">
      < Revenir à l'accueil
    </a>

    <empty-modal id="savingModal" ref="savingModal" no-close="true">
      Questionnaire en cours de publication ...
    </empty-modal>
    <confirm-modal id="savedModal"
                   ref="savedModal"
                   no-close="true"
                   confirmButton="Revenir à l'accueil"
                   @confirm="goHome()">
      Bravo, votre questionnaire est publié!
    </confirm-modal>
  </div>
</template>

<script>
  import axios from "axios"
  import ConfirmModal from '../utils/ConfirmModal'
  import EmptyModal from '../utils/EmptyModal'
  import EventBus from '../events'
  import InfoBar from "../utils/InfoBar"
  import moment from "moment"
  import QuestionnaireBodyCreate from "./QuestionnaireBodyCreate"
  import QuestionnaireMetadataCreate from "./QuestionnaireMetadataCreate"
  import QuestionnairePreview from "./QuestionnairePreview"
  import Vue from "vue"

  // State machine
  const STATES = {
    START : "start",
    // Transition : metadata-created / back
    CREATING_BODY : "creating_body",
    // Transition : body-created / back
    PREVIEW: "preview"
  };

  const get_questionnaire_url = "/api/questionnaire/"
  const save_questionnaire_url = "/api/questionnaire/"
  const home_url = "/accueil/"
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
        errors: [],
        hasErrors: false,
        STATES: STATES,
        questionnaire: {},
        state: "",
        message: "",
        home_url: home_url,
      }
    },
    components: {
      ConfirmModal,
      EmptyModal,
      InfoBar,
      QuestionnaireBodyCreate,
      QuestionnaireMetadataCreate,
      QuestionnairePreview,
    },
    mounted() {
      console.debug('questionnaireId', this.questionnaireId)
      console.debug('controlId', this.controlId)
      if (!this.controlId && !this.questionnaireId) {
        throw 'QuestionnaireCreate needs a controlId or a questionnaireId'
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
        this.emitQuestionnaireUpdated()
        console.debug('questionnaire', this.questionnaire)
        console.log('questionnaire', this.questionnaire)
        this.moveToState(STATES.START)
      },
      _loadQuestionnaireUpdate: function() {
        console.debug('Fetching draft questionnaire...')
        axios.get(get_questionnaire_url + this.questionnaireId)
            .then(response => {
              console.debug('Got draft : ', response.data)
              if (response.data.is_draft !== undefined && !response.data.is_draft) {
                const errorMessage = 'Le questionnaire ' + response.data.id +
                    ' n\'est pas un brouillon. Vous ne pouvez pas le modifier.'
                this.displayErrors(errorMessage)
                return
              }
              this.questionnaire = response.data
              this.emitQuestionnaireLoaded()
              this.emitQuestionnaireUpdated()
              this.moveToState(STATES.START)
            }).catch(error => {
              this.displayErrors('Erreur lors du chargement du brouillon.', error.response.data)
            })
      },
      emitQuestionnaireLoaded: function() {
        this.$emit('questionnaire-loaded', this.questionnaire)
      },
      emitQuestionnaireUpdated: function() {
        this.$emit('questionnaire-updated', this.questionnaire)
      },
      moveToState: function(newState) {
        this.clearErrors()
        this.state = newState;
      },
      onBodyCreated: function(body) {
        console.debug('QuestionnaireCreate got body', body);
        this._updateBody(body);
        this.saveDraft()
        this.emitQuestionnaireUpdated();
        this.moveToState(STATES.PREVIEW);
      },
      _updateBody(body) {
        this.questionnaire.themes = body;
      },
      onMetadataCreated: function(metadata) {
        console.debug('got metadata', metadata);
        this._updateMetadata(metadata)
        this.saveDraft()
        this.emitQuestionnaireUpdated();
        this.moveToState(STATES.CREATING_BODY);
      },
      _updateMetadata: function(metadata) {
        for (const [key, value] of Object.entries(metadata)) {
          this.questionnaire[key] = value
        }
      },
      _updateQuestionnaire: function(questionnaire) {
        this.questionnaire.id = questionnaire.id
        this.questionnaire.description = questionnaire.description
        this.questionnaire.end_date = questionnaire.end_date
        this.questionnaire.title = questionnaire.title
        this._updateBody(questionnaire.themes)
      },
      back: function() {
        console.debug('back');
        if (this.state === STATES.CREATING_BODY) {
          this.saveDraft()
          this.emitQuestionnaireUpdated();
          this.moveToState(STATES.START);
          return;
        }
        if (this.state === STATES.PREVIEW) {
          this.moveToState(STATES.CREATING_BODY)
          return;
        }
        console.error('Trying to go back from state', this.state);
      },
      displayErrors: function(errorMessage, errors) {
        this.hasErrors = true
        this.errors = errors
        if (errors) {
          this.errorMessage = errorMessage + " Erreurs : " + JSON.stringify(errors)
        } else {
          this.errorMessage = errorMessage
        }
        console.error(errorMessage)
      },
      clearErrors() {
        this.hasErrors = false
        this.errors = []
        this.errorMessage = ""
      },
      clearMessages() {
        this.message = ""
      },
      _doSave() {
        const cleanPreSave = () => {
          if (this.questionnaire.end_date) {
            this.questionnaire.end_date = moment(String(this.questionnaire.end_date)).format('YYYY-MM-DD')
          } else {
            delete this.questionnaire.end_date  // remove empty strings, it throws date format error.
          }

          console.debug('Questionnaire to save : ', this.questionnaire)
        }

        this.clearErrors()
        cleanPreSave()

        let saveMethod = axios.post.bind(this, save_questionnaire_url)
        if (this.questionnaire.id !== undefined) {
          console.debug('questionnaire', this.questionnaire)
          saveMethod = axios.put.bind(this, save_questionnaire_url + this.questionnaire.id + '/')
        }
        return saveMethod(this.questionnaire)
            .then(response => {
              console.debug(response)
              this._updateQuestionnaire(response.data)
              this.emitQuestionnaireUpdated()

              const timeString = moment(new Date()).format('HH:mm:ss')
              this.message = "Votre dernière sauvegarde a eu lieu à " + timeString + "."
            }).catch(error => {
              console.error(error)
              this.displayErrors('Erreur lors de la sauvegarde du brouillon.', error.response.data)
            })
      },
      saveDraftFromMetadata(data) {
        this._updateMetadata(data)
        this.saveDraft()
      },
      saveDraftFromBody(data) {
        console.debug('saveDraftFromBody', data)
        this._updateBody(data)
        this.saveDraft()
      },
      saveDraft() {
        this.questionnaire.is_draft = true
        this._doSave()
      },
      fakeSave() {
        // Create a promise that rejects in <ms> milliseconds
        return new Promise((resolve, reject) => {
          let id = setTimeout(() => {
            clearTimeout(id);
            resolve()
          }, 3000)
        })
      },
      saveNonDraft() {
        $(this.$refs.savingModal.$el).modal('show')
        this.questionnaire.is_draft = false
        this._doSave()
            .then(() => {
              $(this.$refs.savingModal.$el).modal('hide')
              $(this.$refs.savedModal.$el).modal('show')
            })
      },
      goHome() {
        window.location.href = home_url
      },
    }
  });
</script>

<style></style>
