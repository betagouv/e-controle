<template>
  <div class="card-header border-0 p-0">
    <span class="stamp stamp-md bg-blue mr-3" style="cursor: pointer">
      {{ themeNumbering }}.{{ questionNumbering }}
    </span>

    <div class="card-text" style="cursor: pointer;">
      <div class="with-line-breaks">{{ questionDescription }}</div>
      <div class="tags">
        <template v-if="questionFileCount > 0">
          <span class="tag tag-orange pull-left">
            {{ questionFileCount }} fichier{{ questionFileCount===1 ? '': 's' }} annexe{{ questionFileCount===1 ? '': 's' }}
            <span class="tag-addon">
              <i class="fe fe-paperclip"></i>
            </span>
          </span>
        </template>
        <template v-if="responseFileCount">
          <span class="tag tag-azure pull-left" style="cursor: pointer">
            {{responseFileCount}} fichier{{ responseFileCount===1 ? '': 's' }} déposé{{ responseFileCount===1 ? '': 's' }}
            <span class="tag-addon">
              <i class="fe fe-file"></i>
            </span>
          </span>
        </template>
      </div>
    </div>
  </div>
</template>

<script lang="ts">

  import Vue from "vue";

  import EventBus from '../events'

  export default Vue.extend({
    data() {
      return {
          questionFileCount: 0,
          responseFileCount: 0,
      };
    },
    mounted() {
      // todo get the original response-file-count from props, instead of event from questionnaire-detail.js
      EventBus.$on('response-file-count-updated-' + this.questionId, responseFileCount => {
        this.responseFileCount = responseFileCount;
      })

      EventBus.$on('question-file-count-changed-' + this.questionId, (questionFileCount) => {
        this.questionFileCount = questionFileCount;
      })

    },
    components: {
    },
    props: {
      themeNumbering: String|Number,
      questionNumbering: String|Number,

      // todo get these 3 from the question object once we switch all to Vue
      questionDescription: String,
      questionId: String|Number,
    },
    methods: {},
  });
</script>

<style scoped>

</style>
