import User from './users/User.vue'
import Vue from 'vue/dist/vue.js'

const EventBus = new Vue();
export default EventBus;

var vm1 = new Vue({
  el: '#vm-app-1',
  data: {
  },
  components: {
    User
  },
});
