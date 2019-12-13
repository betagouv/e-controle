import "@babel/polyfill"
import './utils/polyfills.js'

import { mapActions } from 'vuex'
import { store } from "./store"
import QuestionnaireCreate from './questionnaires/QuestionnaireCreate.vue'
import Vue from 'vue/dist/vue.js'
import Vuex from 'vuex'

Vue.use(Vuex);


new Vue({
  store,
  el: '#questionnaire-create-vm',
  data: {
  },
  components: {
    QuestionnaireCreate,
  },
  methods: {
    ...mapActions(['loadConfig']),
  },
  created() {
    this.loadConfig()
  },
});
