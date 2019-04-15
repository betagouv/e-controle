<template>
  <div>
    <questionnaire-metadata-create ref="createMetadataChild" v-show="state === STATES.START">
    </questionnaire-metadata-create>
    <questionnaire-body-create ref="createBodyChild" v-show="state === STATES.METADATA_CREATED">
    </questionnaire-body-create>
    <div v-show="state === STATES.DONE">
      All done! {{questionnaire}}
    </div>
  </div>
</template>

<script>
  import Vue from "vue";
  import QuestionnaireBodyCreate from "./QuestionnaireBodyCreate"
  import QuestionnaireMetadataCreate from "./QuestionnaireMetadataCreate"

  let STATES = {
    START : "start",
    METADATA_CREATED : "metadata_created",
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
      QuestionnaireMetadataCreate
    },
    mounted() {
      this.$refs.createMetadataChild.$on('metadata-created', functiocon(data) {
        console.log('got metadata', data);
        // "this" is the child component.
        this.$parent.questionnaire.metadata = data;
        this.$parent.state = STATES.METADATA_CREATED;
      });

      this.$refs.createBodyChild.$on('body-created', function(data) {
        console.log('got body', data);
        // "this" is the child component.
        this.$parent.questionnaire.body = data;
        this.$parent.state = STATES.DONE;
      })

    }
  });
</script>

<style></style>
