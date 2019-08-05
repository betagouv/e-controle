import "@babel/polyfill"

import InfoBar from './utils/InfoBar'
import QuestionBox from './questions/QuestionBox'
import QuestionFileList from './questions/QuestionFileList'
import ResponseDropzone from './questions/ResponseDropzone'
import ResponseFileList from './questions/ResponseFileList'
import QuestionnaireDetailPage from './questionnaires/QuestionnaireDetailPage'
import Vue from 'vue/dist/vue.js'

let question_app = new Vue({
  el: '#questionnaire-detail-app',
  components: {
    InfoBar,
    QuestionBox,
    QuestionFileList,
    ResponseDropzone,
    ResponseFileList,
    QuestionnaireDetailPage,
  },
});
