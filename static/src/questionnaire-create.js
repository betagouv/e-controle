import "@babel/polyfill"
import './utils/polyfills.js'

import Vue from 'vue/dist/vue.js'

import QuestionnaireCreate from './questionnaires/QuestionnaireCreate.vue'

new Vue({
  el: '#questionnaire-create-vm',
  data: {
  },
  components: {
    QuestionnaireCreate,
  },
});
