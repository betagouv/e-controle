import "@babel/polyfill"

import { mapActions } from 'vuex'
import Vue from 'vue/dist/vue.js'
import Vuex from 'vuex'

import { store } from "./store"
import ControlPage from './controls/ControlPage'

Vue.use(Vuex);

new Vue({
  store,
  el: '#questionnaire-list-vm',
  components: {
    ControlPage,
  },
  methods: {
    ...mapActions(['setSessionUser']),
  },
  created() {
    this.setSessionUser()
  },
});
