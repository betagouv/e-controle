import '@babel/polyfill'
import './utils/polyfills.js'

import { mapFields } from 'vuex-map-fields'
import { store } from './store'
import QuestionnaireCreate from './questionnaires/QuestionnaireCreate.vue'
import Vue from 'vue/dist/vue.js'
import Vuex, { mapActions } from 'vuex'

Vue.use(Vuex)

let questionnaireCreate = new Vue({
  store,
  el: '#questionnaire-create-vm',
  computed: {
    ...mapFields([
      'sessionUser',
    ]),
  },
  components: {
    QuestionnaireCreate,
  },
  methods: {
    ...mapActions(['loadConfig', 'fetchSessionUser']),

  },
  created() {
    this.loadConfig()
    this.fetchSessionUser()
  },
})
