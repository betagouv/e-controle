import 'babel-polyfill'
import Vue from 'vue/dist/vue.js'

import ControlCreate from './controls/ControlCreate.vue'

new Vue({
  el: '#control-create-vm',
  data: {
  },
  components: {
    ControlCreate,
  },
});
