<template>
  <div>
    <questionnaire-metadata-create
            ref="createMetadataChild"
            v-show="state === STATES.START">
    </questionnaire-metadata-create>
    <questionnaire-body-create
            ref="createBodyChild"
            v-show="state === STATES.METADATA_CREATED">
    </questionnaire-body-create>
    <questionnaire-preview
            ref="previewChild"
            v-show="state === STATES.DONE">
    </questionnaire-preview>
  </div>
</template>

<script>
  import Vue from "vue";
  import QuestionnaireBodyCreate from "./QuestionnaireBodyCreate"
  import QuestionnaireMetadataCreate from "./QuestionnaireMetadataCreate"
  import QuestionnairePreview from "./QuestionnairePreview";

  // State machine
  let STATES = {
    START : "start",
    // Transition : metadata-created / back
    METADATA_CREATED : "metadata_created",
    // Transition : body-created / back
    DONE: "done"
  };

  export default Vue.extend({
    data() {
      return {
        STATES : STATES,
        questionnaire: {},
        state: STATES.START
      }
    },
    methods: {
    },
    components: {
      QuestionnaireBodyCreate,
      QuestionnaireMetadataCreate,
      QuestionnairePreview
    },
    mounted() {
      let emitQuestionnaireUpdated = function() {
        this.$emit('questionnaire-updated', this.questionnaire);
      }.bind(this);

      let moveToState = function(newState) {
        this.state = newState;
      }.bind(this);

      emitQuestionnaireUpdated();

      this.$refs.createMetadataChild.$on('metadata-created', function(data) {
        console.log('got metadata', data);
        // "this" is the child component.
        this.$parent.questionnaire.metadata = data;
        emitQuestionnaireUpdated();
        moveToState(STATES.METADATA_CREATED);
      });

      this.$refs.createBodyChild.$on('body-created', function(data) {
        console.log('got body', data);
        // "this" is the child component.
        this.$parent.questionnaire.body = data;
        emitQuestionnaireUpdated();
        moveToState(STATES.DONE);
      });


      let setupBack = function(childRef, newState) {
        this.$refs[childRef].$on('back', function() {
          console.log('back');
          moveToState(newState);
        });
      }.bind(this);

      setupBack('createBodyChild', STATES.START);
      setupBack('previewChild', STATES.METADATA_CREATED);

    }
  });
</script>

<style></style>
