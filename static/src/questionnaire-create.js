import '@babel/polyfill'
import './utils/polyfills.js'

import Vuex, { mapActions } from 'vuex'
import { store } from './store'
import QuestionnaireCreate from './questionnaires/QuestionnaireCreate.vue'
import Vue from 'vue/dist/vue.js'

Vue.use(Vuex)

// eslint-disable-next-line no-new
new Vue({
  store,
  el: '#questionnaire-create-vm',
  data: {
  },
  components: {
    QuestionnaireCreate,
  },
  methods: {
    ...mapActions(['loadConfig', 'fetchControls']),
  },
  created() {
    this.loadConfig()
    this.fetchControls()
  },
})
