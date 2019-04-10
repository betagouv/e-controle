import Vue from 'vue/dist/vue.js'
import UserList from './users/UserList.vue'
import UserCreate from './users/UserCreate.vue'
import Vuex from 'vuex'

import { store } from './store/store';
import { mapActions } from 'vuex'

Vue.use(Vuex);


var control_app = new Vue({
  el: '#control-section',
  data: {
  },
  store,
  components: {
    UserList,
    UserCreate
  },
  methods: {
    ...mapActions(['loadData']),
  },
  created() {
    this.loadData()
  }
});
