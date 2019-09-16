import "@babel/polyfill"

import { mapActions } from 'vuex'
import { store } from "./store"
import Vue from 'vue/dist/vue.js'
import Vuex from 'vuex'

import AddUserModal from "./users/AddUserModal"
import axios from "axios"
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

const get_questionnaire_url = "/api/questionnaire/"

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
    publish: function(questionnaireId) {
      console.log('publish', questionnaireId)
/*      axios.get(get_questionnaire_url + this.questionnaireId)
          .then(response => {
            console.debug('Got draft : ', response.data)
            if (response.data.is_draft !== undefined && !response.data.is_draft) {
              const errorMessage = 'Le questionnaire ' + response.data.id +
                  ' n\'est pas un brouillon. Vous ne pouvez pas le modifier.'
              this.displayErrors(errorMessage)
              return
            }
            this.questionnaire = response.data
            this.emitQuestionnaireLoaded()
            this.emitQuestionnaireUpdated()
            this.moveToState(STATES.START)
          }).catch(error => {
            this.displayErrors('Erreur lors du chargement du brouillon.', error.response.data)
          })*/
    },
  },
  created() {
    this.setSessionUser()
  }
});
