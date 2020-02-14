import '@babel/polyfill'
import './utils/polyfills.js'

import { store } from './store'
import QuestionnaireCreate from './questionnaires/QuestionnaireCreate.vue'
import routes from './routes'
import Vue from 'vue/dist/vue.js'
import VueRouter from 'vue-router'
import Vuex, { mapActions } from 'vuex'

Vue.use(VueRouter)
Vue.use(Vuex)

const router = new VueRouter({
  routes,
})

// Note : the parcel builds (build-questionnaire-create and watch-questionnaire-create) use
// --no-source-maps, because vuejs-datepicker breaks parcel without it.

// eslint-disable-next-line no-new
new Vue({
  store,
  router,
  el: '#questionnaire-create-vm',
  components: {
    QuestionnaireCreate,
  },
  methods: {
    ...mapActions(['fetchConfig', 'fetchControls', 'fetchSessionUser']),
  },
  created() {
    this.fetchConfig()
    this.fetchControls()
    this.fetchSessionUser()
  },
})
