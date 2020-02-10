import '@babel/polyfill'
import './utils/polyfills.js'

import QuestionnaireDetailPage from './questionnaires/QuestionnaireDetailPage'
import Vue from 'vue/dist/vue.js'
import Vuex, { mapActions } from 'vuex'
import { store } from './store'

Vue.use(Vuex)

// eslint-disable-next-line no-new
new Vue({
  store,
  el: '#questionnaire-detail-app',
  components: {
    QuestionnaireDetailPage,
  },
  methods: {
    ...mapActions(['fetchConfig', 'fetchSessionUser']),
  },
  created() {
    this.fetchConfig()
    this.fetchSessionUser()
  },
})
