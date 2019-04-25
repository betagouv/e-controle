<template>
  <div class="card-header border-1" data-toggle="card-collapse">
    <span class="stamp stamp-md bg-blue mr-3" style="cursor: pointer">
      {{ theme_numbering }}.{{ question_numbering }}
    </span>
    <div class="card-text" style="cursor: pointer">
      {{ question_description }}
      <div class="tags">
        <template v-if="answers_number">
          <span class="tag tag-azure pull-left" style="cursor: pointer">
            {{answers_number}} fichier{{ answers_number===1 ? '': 's' }} déposé{{ answers_number===1 ? '': 's' }}
            <span class="tag-addon">
              <i class="fe fe-file"></i>
            </span>
          </span>
        </template>
        <template v-if="annexes_number">
          <span class="tag tag-orange pull-left">
            {{ annexes_number }} fichier{{ annexes_number===1 ? '': 's' }} annexe{{ annexes_number===1 ? '': 's' }}
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

  import axios from 'axios';
  import Vue from "vue";
  import VueAxios from 'vue-axios';

  export default Vue.extend({
    data() {
      return {answers_number: 0};
    },
    mounted() {
      var _this = this
      this.$parent.$on('question-updated-' + this.question_id, function (answer_number) {
        _this.answers_number = answer_number;
      })
    },
    props: {
      question_description: String,
      theme_numbering: String,
      question_numbering: String,
      question_id: String,
      annexes_number: String,
    },
    methods: {}
  });
</script>

<style scoped>

</style>