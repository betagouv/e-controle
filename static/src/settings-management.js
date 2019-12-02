import "@babel/polyfill"

import Vue from 'vue/dist/vue.js'
import LoadSettings from './settings/LoadSettings'

new Vue({
  el: '#settings-management-vm',
  components: {
    LoadSettings,
  }
});
