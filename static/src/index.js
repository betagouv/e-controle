import Vue from 'vue/dist/vue.js'
import User from './users/User.vue'

var useHandler = new Vue({
  el: '#questionnaire-list-app',
  data: {
  },
  components: {
    User,
  },
});
