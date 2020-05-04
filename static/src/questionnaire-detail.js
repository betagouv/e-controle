import '@babel/polyfill'
import './utils/polyfills.js'

import QuestionnaireDetailPage from './questionnaires/QuestionnaireDetailPage'
import Vue from 'vue/dist/vue.js'
import Vuex, { mapActions } from 'vuex'
import { store } from './store'

Vue.use(Vuex)

/*
XSS-safe way to get JSON data from server : write it to html (django template does html encoding)
and then fetch it into JS using safe DOM manipulation functions.
Source :
https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html#html-entity-encoding

A simpler safe way to get unsafe server data into Vue would be to get it through an AJAX request,
instead of passing it through server templates.
It does adds a delay for the user, since they will wait for the ajax-requested data.
*/
const controlDataEl = document.getElementById('control-data')
// decode and parse the content of the div
const control = JSON.parse(controlDataEl.textContent)

// This data is safe because not user-provided. But we have to get it like this too.
const questionnaireIdDataEl = document.getElementById('questionnaire-id-data')
const questionnaireId = Number(questionnaireIdDataEl.textContent.trim())

// eslint-disable-next-line no-new
new Vue({
  store,
  el: '#questionnaire-detail-app',
  render: h => h(
    QuestionnaireDetailPage,
    {
      props: {
        control: control,
        questionnaireId: questionnaireId,
      },
    }),
  methods: {
    ...mapActions(['fetchConfig', 'fetchSessionUser']),
  },
  created() {
    this.fetchConfig()
    this.fetchSessionUser()
  },
})
