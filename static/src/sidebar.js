import '@babel/polyfill'
import './utils/polyfills.js'

import Sidebar from './utils/Sidebar'
import Vue from 'vue'

new Vue({ // eslint-disable-line no-new
  el: '#sidebar-vm',
  components: {
    Sidebar,
  },
});
