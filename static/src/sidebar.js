import "@babel/polyfill"

import Sidebar from './utils/Sidebar'
import Vue from 'vue/dist/vue.js'

new Vue({
  el: '#sidebar-vm',
  components: {
    Sidebar,
  },
});
