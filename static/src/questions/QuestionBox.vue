<template>
  <div v-bind:id="'question' + themeNumbering + '.' + questionNumbering"
       class="card m-0 p-0 pb-0">
    <div class="card-header border-0" data-toggle="card-collapse">
      <question :question_description="question.description"
                :theme_numbering="themeNumbering"
                :question_numbering="questionNumbering"
                :question_id="question.id"
                :annexe_count="question.question_files && question.question_files.length">
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
      'themeNumbering',
      'questionNumbering',
      'question'
    ],
    components: {
      Question,
    },
  })
</script>