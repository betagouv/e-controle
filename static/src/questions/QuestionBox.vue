<template>
  <div v-bind:id="'question' + themeNumbering + '-' + questionNumbering"
       class="card m-0 p-0 pb-0">
    <div class="card-header border-0"
         :data-toggle="collapseValue"
         :data-target="'#question-body-' + question.id">
      <question :theme-numbering="themeNumbering"
                :question-numbering="questionNumbering"
                :question="question">
      </question>
    </div>
    <div :class="collapseValue" :id="'question-body-' + question.id">
      <slot></slot>
    </div>

  </div>
</template>

<script>
import Question from './Question'
import Vue from 'vue'

export default Vue.extend({
  props: {
    question: Object,
    questionNumbering: Number,
    themeNumbering: Number,
    // Note : tabler.io's card-collapse doesn't work within a v-for. So we use bootstrap collapse.
    withCollapse: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    collapseValue: function() {
      if (this.withCollapse) return 'collapse'
      return ''
    },
  },
  components: {
    Question,
  },
})
</script>
