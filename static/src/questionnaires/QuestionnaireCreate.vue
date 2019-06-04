<template>
  <div>
    <questionnaire-metadata-create
            ref="createMetadataChild"
            v-on:metadata-created="metadataCreated"
            v-show="state === STATES.START">
    </questionnaire-metadata-create>
    <questionnaire-body-create
            ref="createBodyChild"
            v-on:body-created="bodyCreated"
            v-on:back="back"
            v-show="state === STATES.CREATING_BODY">
    </questionnaire-body-create>
    <questionnaire-preview
            ref="previewChild"
            v-on:back="back"
            v-show="state === STATES.PREVIEW">
    </questionnaire-preview>
  </div>
</template>

<script>
  import axios from "axios"
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
  axios.defaults.xsrfCookieName = 'csrftoken'
  axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'

  export default Vue.extend({
    props: {
      controlId: Number,
      questionnaireId: Number,
    },
    data() {
      return {
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
            this.emitQuestionnaireUpdated()
            this.moveToState(STATES.START)
          }).catch(error => {
            // todo display error
            console.log(error.response.data)
          })
    },
    methods: {
      emitQuestionnaireUpdated: function() {
        this.$emit('questionnaire-updated', this.questionnaire)
      },
      moveToState: function(newState) {
        this.state = newState;
      },
      bodyCreated: function(data) {
        console.log('got body', data);
        this.questionnaire.themes = data;
        this.emitQuestionnaireUpdated();
        this.moveToState(STATES.PREVIEW);
      },
      metadataCreated: function(data) {
        console.log('got metadata', data);
        for (const [key, value] of Object.entries(data)) {
          this.questionnaire[key] = value
        }
        this.emitQuestionnaireUpdated();
        this.moveToState(STATES.CREATING_BODY);
      },
      back: function() {
        console.log('back');
        if (this.state === STATES.CREATING_BODY) {
          this.moveToState(STATES.START);
          return;
        }
        if (this.state === STATES.PREVIEW) {
          this.moveToState(STATES.CREATING_BODY)
          return;
        }
        console.error('Trying to go back from state', this.state);
      }
    }
  });
</script>

<style></style>
