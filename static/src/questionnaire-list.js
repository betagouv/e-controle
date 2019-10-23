import "@babel/polyfill"

import { mapActions } from 'vuex'
import Vue from 'vue/dist/vue.js'
import Vuex from 'vuex'

import { store } from "./store"
import AddUserModal from "./users/AddUserModal"
import ControlCreate from "./controls/ControlCreate"
import ControlListSidebar from './controls/ControlListSidebar'
import ControlTitle from "./controls/ControlTitle"
import HelpTooltip from "./utils/HelpTooltip"
import RemoveUserModal from "./users/RemoveUserModal"
import UpdateUserModal from "./users/UpdateUserModal"
import UserSection from './users/UserSection'
import VideoModal from "./utils/VideoModal"
import WebdavTip from './controls/WebdavTip'

Vue.use(Vuex);

new Vue({
  store,
  el: '#questionnaire-list-vm',
  components: {
    AddUserModal,
    ControlCreate,
    ControlListSidebar,
    ControlTitle,
    HelpTooltip,
    RemoveUserModal,
    UpdateUserModal,
    UserSection,
    VideoModal,
    WebdavTip
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
