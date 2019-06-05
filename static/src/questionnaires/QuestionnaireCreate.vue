<template>
  <div>
    <div class="page-header">
      <div class="page-title">
        Nouveau questionnaire
      </div>
    </div>
    <div v-if="hasErrors" class="alert alert-danger">
      L'envoi de ce formulaire n'a pas fonctionné. Erreur : {{JSON.stringify(errors)}}
    </div>
    <questionnaire-metadata-create
            ref="createMetadataChild"
            v-on:metadata-created="metadataCreated"
            v-on:save-draft="saveDraftFromMetadata"
            v-show="state === STATES.START">
    </questionnaire-metadata-create>
    <questionnaire-body-create
            ref="createBodyChild"
            v-on:body-created="bodyCreated"
            v-on:save-draft="saveDraftFromBody"
            v-on:back="back"
            v-show="state === STATES.CREATING_BODY">
    </questionnaire-body-create>
    <questionnaire-preview
            ref="previewChild"
            v-on:save-questionnaire="saveNonDraft"
            v-on:back="back"
            v-show="state === STATES.PREVIEW">
    </questionnaire-preview>
  </div>
</template>

<script>
  import axios from "axios"
  import moment from "moment"
  import Vue from "vue"
  import QuestionnaireBodyCreate from "./QuestionnaireBodyCreate"
  import QuestionnaireMetadataCreate from "./QuestionnaireMetadataCreate"
  import QuestionnairePreview from "./QuestionnairePreview"

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
    },
    data() {
      return {
        errors: [],
        hasErrors: false,
        STATES : STATES,
        questionnaire: {},
        state: ""
      }
    },
    components: {
      QuestionnaireBodyCreate,
      QuestionnaireMetadataCreate,
      QuestionnairePreview
    },
    mounted() {
      console.log('questionnaireId', this.questionnaireId)
      console.log('controlId', this.controlId)
      if (!this.controlId && !this.questionnaireId) {
        throw 'QuestionnaireCreate needs a controlId or a questionnaireId'
      }

      if (typeof this.controlId !== 'undefined') {
        this.questionnaire.control = this.controlId
        this.emitQuestionnaireUpdated()
        console.log('questionnaire', this.questionnaire)
        this.moveToState(STATES.START)
        return
      }

      console.log('Fetching draft questionnaire...')
      axios.get(get_questionnaire_url + this.questionnaireId)
          .then(response => {
            console.log('Got draft : ', response.data)
            // todo : check that it's a draft questionnaire
            this.questionnaire = response.data
            this.emitQuestionnaireLoaded()
            this.emitQuestionnaireUpdated()
            this.moveToState(STATES.START)
          }).catch(error => {
            // todo display error
            console.log(error.response.data)
          })
    },
    methods: {
      emitQuestionnaireLoaded: function() {
        this.$emit('questionnaire-loaded', this.questionnaire)
      },
      emitQuestionnaireUpdated: function() {
        this.$emit('questionnaire-updated', this.questionnaire)
      },
      moveToState: function(newState) {
        this.state = newState;
      },
      bodyCreated: function(data) {
        console.log('got body', data);
        this._updateBody(data);
        this.emitQuestionnaireUpdated();
        this.moveToState(STATES.PREVIEW);
      },
      _updateBody(data) {
        this.questionnaire.themes = data;
      },
      metadataCreated: function(data) {
        console.log('got metadata', data);
        this._updateMetadata(data)
        this.emitQuestionnaireUpdated();
        this.moveToState(STATES.CREATING_BODY);
      },
      _updateMetadata: function(data) {
        for (const [key, value] of Object.entries(data)) {
          this.questionnaire[key] = value
        }
      },
      back: function() {
        console.log('back');
        this.clearErrors()
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
      clearErrors() {
        this.errors = []
        this.hasErrors = false
      },
      _doSave() {
        const cleanPreSave = () => {
          if (this.questionnaire.end_date) {
            this.questionnaire.end_date = moment(String(this.questionnaire.end_date)).format('YYYY-MM-DD')
          } else {
            delete this.questionnaire.end_date  // remove empty strings, it throws date format error.
          }

          console.log('Questionnaire to save : ', this.questionnaire)
        }

        this.clearErrors()
        cleanPreSave()

        let saveMethod = axios.post.bind(this, save_questionnaire_url)
        if (this.questionnaire.id !== undefined) {
          console.log('qr', this.questionnaire)
          console.log('qr id', this.questionnaire.id)
          saveMethod = axios.put.bind(this, save_questionnaire_url + this.questionnaire.id + '/')
        }
        return saveMethod(this.questionnaire)
            .then(response => {
              console.log(response)
            }).catch(error => {
              console.log(error)
              this.hasErrors = true
              this.errors = error.response.data
            })
      },
      saveDraftFromMetadata(data) {
        this._updateMetadata(data)
        this._saveDraft()
      },
      saveDraftFromBody(data) {
        console.log('saveDraftFromBody', data)
        this._updateBody(data)
        this._saveDraft()
      },
      _saveDraft() {
        this.questionnaire.is_draft = true
        this._doSave()
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
