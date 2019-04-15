import Users from './users/Users.vue'
import Vue from 'vue/dist/vue.js'
import QuestionnaireCreate from './questionnaires/QuestionnaireCreate.vue'

var vm1 = new Vue({
  el: '#questionnaire-list-vm',
  data: {
  },
  components: {
    'users-for-control': Users
  },
});

var questionnaireCreate = new Vue({
  el: '#questionnaire-create-vm',
  data: {
  },
  components: {
    QuestionnaireCreate,
  },
});
