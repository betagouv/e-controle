<template>
  <div class="card-header border-0 p-0">
    <span class="stamp stamp-md bg-blue mr-3" style="cursor: pointer">
      {{ theme_numbering }}.{{ question_numbering }}
    </span>

    <div class="card-text" style="cursor: pointer;">
      <div class="with-line-breaks">{{ question_description }}</div>
      <div class="tags">
        <template v-if="annexe_count > 0">
          <span class="tag tag-orange pull-left">
            {{ annexe_count }} fichier{{ annexe_count===1 ? '': 's' }} annexe{{ annexe_count===1 ? '': 's' }}
            <span class="tag-addon">
              <i class="fe fe-paperclip"></i>
            </span>
          </span>
        </template>
        <template v-if="answer_count">
          <span class="tag tag-azure pull-left" style="cursor: pointer">
            {{answer_count}} fichier{{ answer_count===1 ? '': 's' }} déposé{{ answer_count===1 ? '': 's' }}
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
      return {answer_count: 0};
    },
    mounted() {
      var _this = this
      EventBus.$on('answercount-updated-' + this.question_id, function (answer_count) {
        _this.answer_count = answer_count;
      })
    },
    components: {
    },
    props: {
      question_description: String,
      theme_numbering: String|Number,
      question_numbering: String|Number,
      question_id: String|Number,
      annexe_count: String|Number,
    },
    methods: {},
  });
</script>

<style scoped>

</style>
