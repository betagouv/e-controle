<template>
  <div class="card-header border-1" data-toggle="card-collapse">
    <span class="stamp stamp-md bg-blue mr-3" style="cursor: pointer">
      {{ theme_numbering }}.{{ question_numbering }}
    </span>
    <div class="card-text" style="cursor: pointer">
      {{ question_description }}
      <div class="tags">
        <template v-if="answer_count">
          <span class="tag tag-azure pull-left" style="cursor: pointer">
            {{answer_count}} fichier{{ answer_count===1 ? '': 's' }} déposé{{ answer_count===1 ? '': 's' }}
            <span class="tag-addon">
              <i class="fe fe-file"></i>
            </span>
          </span>
        </template>
        <template v-if="annexe_count">
          <span class="tag tag-orange pull-left">
            {{ annexe_count }} fichier{{ annexe_count===1 ? '': 's' }} annexe{{ annexe_count===1 ? '': 's' }}
            <span class="tag-addon">
              <i class="fe fe-paperclip"></i>
            </span>
          </span>
        </template>
      </div>
    </div>
  </div>
</template>

<script lang="ts">

  import Vue from "vue";

  export default Vue.extend({
    data() {
      return {answer_count: 0};
    },
    mounted() {
      var _this = this
      this.$parent.$on('question-updated-' + this.question_id, function (answer_count) {
        _this.answer_count = answer_count;
      })
    },
    props: {
      question_description: String,
      theme_numbering: String,
      question_numbering: String,
      question_id: String,
      annexe_count: String,
    },
    methods: {}
  });
</script>

<style scoped>

</style>