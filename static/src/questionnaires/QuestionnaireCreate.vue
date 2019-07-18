<template>
  <div>
    <div class="page-header">
      <div class="page-title">
        Rédaction du questionnaire n°{{ questionnaireNumbering }} <span v-if="questionnaire"> - {{ questionnaire.title }}</span>
      </div>
    </div>
    <div v-if="hasErrors" class="alert alert-danger">
      L'envoi de ce formulaire n'a pas fonctionné. Erreur : {{JSON.stringify(errors)}}
    </div>
    <div class="row justify-content-around mb-6">
      <wizard-step number="1" :class="{ 'active': state==='start' }">Renseigner l'introduction</wizard-step>
      <wizard-step number="2" :class="{ 'active': state==='creating_body' }">Ajouter des questions</wizard-step>
      <wizard-step number="3" :class="{ 'active': state==='preview' }">Aperçu avant publication</wizard-step>
    </div>
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
       style="position:relative; bottom: 143px; left: 2em;">
      < Revenir à l'accueil
    </a>

  </div>
</template>

<script>
  import axios from "axios"
  import moment from "moment"
  import Vue from "vue"
  import EventBus from '../events'
  import QuestionnaireBodyCreate from "./QuestionnaireBodyCreate"
  import QuestionnaireMetadataCreate from "./QuestionnaireMetadataCreate"
  import QuestionnairePreview from "./QuestionnairePreview"
  import WizardStep from "../utils/WizardStep"

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
      QuestionnaireBodyCreate,
      QuestionnaireMetadataCreate,
      QuestionnairePreview,
      WizardStep,
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
                console.error(errorMessage)
                this.displayErrors(errorMessage)
                return
              }
              this.questionnaire = response.data
              this.emitQuestionnaireLoaded()
              this.emitQuestionnaireUpdated()
              this.moveToState(STATES.START)
            }).catch(error => {
          console.error(error)
          this.displayErrors(error.response.data)
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
          this.moveToState(STATES.START);
          return;
        }
        if (this.state === STATES.PREVIEW) {
          this.moveToState(STATES.CREATING_BODY)
          return;
        }
        console.error('Trying to go back from state', this.state);
      },
      displayErrors: function(errors) {
        this.hasErrors = true
        this.errors = errors
      },
      clearErrors() {
        this.errors = []
        this.hasErrors = false
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
            }).catch(error => {
              console.error(error)
              this.displayErrors(error.response.data)
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
            .then(() => {
                const timeString = moment(new Date()).format('HH:mm:ss')
                this.message = "Votre dernière sauvergarde a eu lieu à " + timeString + "."
            })
      },
      saveNonDraft() {
        this.questionnaire.is_draft = false
        this._doSave()
            .then(() => {
              window.location.href = home_url
            })
      }
    }
  });
</script>

<style></style>
