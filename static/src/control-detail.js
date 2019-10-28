import "@babel/polyfill"

import { mapActions } from 'vuex'
import Vue from 'vue/dist/vue.js'
import Vuex from 'vuex'

import { store } from "./store"
import ControlPage from './controls/ControlPage'

Vue.use(Vuex);

new Vue({
  store,
  el: '#control-detail-vm',
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
