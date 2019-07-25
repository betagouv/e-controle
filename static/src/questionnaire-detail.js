import "@babel/polyfill"

import axios from 'axios'
import EventBus from './events'
import InfoBar from './utils/InfoBar'
import Question from './details/Question'
import QuestionFileList from './questionnaires/QuestionFileList'
import ResponseDropzone from './details/ResponseDropzone'
import ResponseFileList from './details/ResponseFileList'
import Vue from 'vue/dist/vue.js'

const url = "/api/question/";

let question_app = new Vue({
  el: '#questionnaire-detail-app',
  data: {},
  methods: {
    fetchQuestionData: function () {
      var _this = this;

      axios.get(url).then(function (response) {
        _this.saveResponseFiles(response.data);
      });
    },
    saveResponseFiles: function (question_data) {
      for (var question_id in question_data) {
        let response_files = question_data[question_id].response_files;
        EventBus.$emit('answercount-updated-' + question_id, response_files.length);
        EventBus.$emit('answer-updated-' + question_id, response_files);
      }
    }
  },
  mounted: function () {
    this.fetchQuestionData();
  },
  components: {
    InfoBar,
    Question,
    QuestionFileList,
    ResponseDropzone,
    ResponseFileList,
  },
});
