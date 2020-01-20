import '@babel/polyfill'

import Vuex, { mapActions } from 'vuex'
import Vue from 'vue/dist/vue.js'

import { store } from './store'
import ControlPage from './controls/ControlPage'

Vue.use(Vuex)

new Vue({ // eslint-disable-line no-new
  store,
  el: '#control-detail-vm',
  components: {
    ControlPage,
  },
  methods: {
    ...mapActions(['fetchSessionUser']),
  },
  created() {
    this.fetchSessionUser()
  },
})
