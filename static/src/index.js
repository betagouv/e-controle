import Vue from 'vue/dist/vue.js'
import UserList from './users/UserList.vue'

var control_app = new Vue({
  delimiters: ['[[', ']]'],
  el: '#control-section',
  data: {
    name: 'Hello World! Ce message vient de Vue.JS !!',
  },
  components: {
    UserList
  }
});
