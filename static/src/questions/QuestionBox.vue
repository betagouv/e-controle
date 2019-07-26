<template>
  <div v-bind:id="'question' + themeNumbering + '.' + questionNumbering"
       class="card m-0 p-0 pb-0">
    <div class="card-header border-0" data-toggle="collapse" :data-target="'#question-body-' + question.id">
      <question :theme-numbering="themeNumbering"
                :question-numbering="questionNumbering"
                :question="question">
      </question>
    </div>
    <div class="card-body collapse" :id="'question-body-' + question.id">
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
    ],
    components: {
      Question,
    },
  })
</script>