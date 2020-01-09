import '@babel/polyfill'
import './utils/polyfills.js'

import InfoBar from './utils/InfoBar'
import QuestionBox from './questions/QuestionBox'
import QuestionFileList from './questions/QuestionFileList'
import ResponseDropzone from './questions/ResponseDropzone'
import ResponseFileList from './questions/ResponseFileList'
import QuestionnaireDetailPage from './questionnaires/QuestionnaireDetailPage'
import Vue from 'vue/dist/vue.js'
import Vuex, { mapActions } from 'vuex'
import { store } from './store'

Vue.use(Vuex)

let questionnaireDetailApp = new Vue({
  store,
  el: '#questionnaire-detail-app',
  components: {
    InfoBar,
    QuestionBox,
    QuestionFileList,
    ResponseDropzone,
    ResponseFileList,
    QuestionnaireDetailPage,
  },
  methods: {
    ...mapActions(['loadConfig', 'fetchSessionUser']),
  },
  created() {
    this.loadConfig()
    this.fetchSessionUser()
  },
})
