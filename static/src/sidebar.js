import "@babel/polyfill"

import Sidebar from './controls/Sidebar'
import Vue from 'vue/dist/vue.js'

new Vue({
  el: '#sidebar-vm',
  components: {
    Sidebar,
  },
});
