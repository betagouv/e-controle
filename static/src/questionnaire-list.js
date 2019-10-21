import "@babel/polyfill"

import { mapActions } from 'vuex'
import Vue from 'vue/dist/vue.js'
import Vuex from 'vuex'

import { store } from "./store"
import AddUserModal from "./users/AddUserModal"
import ControlCreate from "./controls/ControlCreate"
import ControlList from './controls/ControlList'
import ControlListSidebar from './controls/ControlListSidebar'
import RemoveUserModal from "./users/RemoveUserModal"
import UpdateUserModal from "./users/UpdateUserModal"
import VideoModal from "./utils/VideoModal"

Vue.use(Vuex);

new Vue({
  store,
  el: '#questionnaire-list-vm',
  components: {
    AddUserModal,
    ControlCreate,
    ControlList,
    ControlListSidebar,
    RemoveUserModal,
    UpdateUserModal,
    VideoModal,
  },
  methods: {
    ...mapActions(['setSessionUser']),
  },
  created() {
    this.setSessionUser()
  },
  data: function() {
    return {
      hash: "",
    }
  },
  mounted() {
    const updateHash = () => {
      console.log('The hash has changed!', window.location.hash)
      this.hash = window.location.hash
    }

    window.addEventListener(
        'hashchange',
        updateHash,
        false)

    updateHash()

  },

});
