import Vue from 'vue/dist/vue.js'
import User from './users/User.vue'


var vm1 = new Vue({
  el: '#vm-app-1',
  data: {
  },
  components: {
    User
  },
});
