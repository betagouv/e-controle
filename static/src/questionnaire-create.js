import 'babel-polyfill'
import QuestionnaireCreate from './questionnaires/QuestionnaireCreate.vue'
import Vue from 'vue/dist/vue.js'

new Vue({
  el: '#questionnaire-create-vm',
  data: {
  },
  components: {
    QuestionnaireCreate,
  },
});
