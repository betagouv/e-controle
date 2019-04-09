import Vue from 'vue/dist/vue.js'
import UserList from './users/UserList.vue'
import UserCreate from './users/UserCreate.vue'

var control_app = new Vue({
  delimiters: ['[[', ']]'],
  el: '#control-section',
  data: {
  },
  components: {
    UserList,
    UserCreate
  }
});
