import "@babel/polyfill"

import { mapActions } from 'vuex'
import Vue from 'vue/dist/vue.js'
import Vuex from 'vuex'

import { store } from "./store"
import AddUserModal from "./users/AddUserModal"
import ColorBar from "./utils/ColorBar"
import ControlCreate from "./controls/ControlCreate"
import ControlTitle from "./controls/ControlTitle"
import HelpTooltip from "./utils/HelpTooltip"
import PublishQuestionnaireModal from "./questionnaires/PublishQuestionnaireModal"
import RemoveUserModal from "./users/RemoveUserModal"
import UpdateUserModal from "./users/UpdateUserModal"
import Users from './users/Users'
import WebdavTip from './controls/WebdavTip'

Vue.use(Vuex);

new Vue({
  store,
  el: '#questionnaire-list-vm',
  components: {
    'users-for-control': Users,
    AddUserModal,
    ColorBar,
    ControlCreate,
    ControlTitle,
    HelpTooltip,
    PublishQuestionnaireModal,
    RemoveUserModal,
    UpdateUserModal,
    WebdavTip
  },
  methods: {
    ...mapActions(['setSessionUser']),
  },
  created() {
    this.setSessionUser()
  }
});
