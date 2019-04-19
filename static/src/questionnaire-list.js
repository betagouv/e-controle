import Users from './users/Users.vue'
import Vue from 'vue/dist/vue.js'

new Vue({
  el: '#questionnaire-list-vm',
  data: {
  },
  components: {
    'users-for-control': Users
  },
});
