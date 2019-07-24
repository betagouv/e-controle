import "@babel/polyfill"

import Answer from './details/Answer'
import AnswerFileList from './details/AnswerFileList'
import axios from 'axios'
import Dropzone from 'dropzone'
import InfoBar from './utils/InfoBar'
import Question from './details/Question'
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
        this.$emit('question-updated-' + question_id, response_files.length);
        this.$emit('answer-updated-' + question_id, response_files);
      }
    }
  },
  mounted: function () {
    this.fetchQuestionData();
  },
  components: {
    'answer': Answer,
    'answer-file-list': AnswerFileList,
    'info-bar': InfoBar,
    'question': Question,
  },
});

Dropzone.options.dropzoneArea = {
  success: function success(file, done) {
    question_app.fetchQuestionData();
  }
};
