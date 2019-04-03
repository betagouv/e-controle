"use strict";

// ES6Promise.polyfill()

import axios from "axios";
import Vue from "vue";
import Dropzone from "dropzone";

var url = "/api/question/";

var question_app = new Vue({
  delimiters: ['[[', ']]'],
  el: '#question-detail-app',
  data: {
    results: {},
    r_files: {}
  },
  methods: {
    fetchQuestionData: function fetchQuestionData() {
      var _this = this;

      axios.get(url).then(function (response) {
        _this.results = response.data;

        _this.saveResponseFiles(response.data);
      });
    },
    saveResponseFiles: function saveResponseFiles(question_data) {
      for (var question_id in question_data) {
        var response_files = question_data[question_id].response_files;

        if (response_files.length == 0) {
          response_files = null;
        }

        this.r_files[question_id] = response_files;
      }
    }
  },
  mounted: function mounted() {
    this.fetchQuestionData();
  }
});
Dropzone.options.dropzoneArea = {
  success: function success(file, done) {
    question_app.fetchQuestionData();
  }
};
