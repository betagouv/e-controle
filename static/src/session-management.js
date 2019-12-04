import "@babel/polyfill"
import './utils/polyfills.js'

import Vue from 'vue/dist/vue.js'
import SessionTimeout from './session/SessionTimeout'

new Vue({
  el: '#session-management-vm',
  components: {
    SessionTimeout,
  }
});
