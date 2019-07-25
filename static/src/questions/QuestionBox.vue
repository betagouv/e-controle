<template>
  <div v-bind:id="'question' + themeNumbering + '.' + questionNumbering"
       class="card m-0 p-0 pb-0">
    <div class="card-header border-0" data-toggle="card-collapse">
      <question v-if="question"
                :question-description="question.description"
                :theme-numbering="themeNumbering"
                :question-numbering="questionNumbering"
                :question-id="question.id">

      </question>
      <question v-else
                :question-description="questionDescription"
                :theme-numbering="themeNumbering"
                :question-numbering="questionNumbering"
                :question-id="questionId">
      </question>
    </div>
    <div class="card-body">
      <slot></slot>
    </div>

  </div>
</template>

<script>
  import Question from './Question'
  import Vue from 'vue'

  export default Vue.extend({
    props: [
      'question',
      'questionNumbering',
      'themeNumbering',

      // todo remove these 3 and the v-else when we switch to all-Vue
      'questionFileCount',
      'questionId',
      'questionDescription',
    ],
    components: {
      Question,
    },
  })
</script>