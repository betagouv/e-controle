<template>
  <div v-bind:id="'question' + themeNumbering + '.' + questionNumbering"
       class="card m-0 p-0 pb-0">
    <div class="card-header border-0" data-toggle="card-collapse">
      <question v-if="question"
                :question_description="question.description"
                :theme_numbering="themeNumbering"
                :question_numbering="questionNumbering"
                :question_id="question.id"
                :annexe_count="question.question_files && question.question_files.length">

      </question>
      <question v-else
                :question_description="questionDescription"
                :theme_numbering="themeNumbering"
                :question_numbering="questionNumbering"
                :question_id="questionId"
                :annexe_count="questionFileCount">
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