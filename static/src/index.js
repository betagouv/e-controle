import Users from './users/Users.vue'
import Vue from 'vue/dist/vue.js'

const EventBus = new Vue();
export default EventBus;

var vm1 = new Vue({
  el: '#questionnaire-list-vm',
  data: {
  },
  components: {
    'users-for-control': Users
  },
});
