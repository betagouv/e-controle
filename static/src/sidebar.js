import '@babel/polyfill'
import './utils/polyfills.js'

import Sidebar from './utils/Sidebar'
import { store } from './store'
import Vue from 'vue/dist/vue.js'
import Vuex from 'vuex'

Vue.use(Vuex)

new Vue({ // eslint-disable-line no-new
  el: '#sidebar-vm',
  store,
  components: {
    Sidebar,
  },
})
