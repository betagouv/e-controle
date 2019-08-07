import "@babel/polyfill"

import Vue from 'vue/dist/vue.js'
import IdleSession from './utils/IdleSession'

new Vue({
  el: '#utils-vm',
  components: {
    IdleSession,
  }
});
