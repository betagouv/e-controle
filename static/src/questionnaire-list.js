import 'babel-polyfill'
import { mapActions } from 'vuex'
import Vue from 'vue/dist/vue.js'
import Vuex from 'vuex'

import { store } from "./store"
import AddUserModal from "./users/AddUserModal"
import Clipboard from 'v-clipboard'
import ColorBar from "./utils/ColorBar"
import ControlCreate from "./controls/ControlCreate"
import HelpTooltip from "./utils/HelpTooltip"
import RemoveUserModal from "./users/RemoveUserModal"
import UpdateUserModal from "./users/UpdateUserModal"
import Users from './users/Users'

Vue.use(Clipboard)
Vue.use(Vuex);

new Vue({
  store,
  el: '#questionnaire-list-vm',
  data: {
    showCopySuccess: false
  },
  components: {
    'users-for-control': Users,
    AddUserModal,
    ColorBar,
    ControlCreate,
    UpdateUserModal,
    RemoveUserModal,
    HelpTooltip
  },
  methods: {
    ...mapActions(['setSessionUser']),

    clipboardSuccessHandler ({ value, event }) {
      this.showCopySuccess = true
    },

    enterFade: function(el, done) {
      var that = this;
      setTimeout(function() {
        that.showCopySuccess = false;
      }, 3000); // hide the message after 3 seconds
    }
  },
  created() {
    this.setSessionUser()
  }
});
