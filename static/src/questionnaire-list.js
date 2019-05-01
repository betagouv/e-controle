import Vue from 'vue/dist/vue.js'

import AddUserModal from "./users/AddUserModal"
import Users from './users/Users'

new Vue({
  el: '#questionnaire-list-vm',
  data: {
  },
  components: {
    'users-for-control': Users,
    AddUserModal
  },
});
