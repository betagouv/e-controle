import Vue from 'vue/dist/vue.js'
import Dropzone from 'dropzone';
import Question from './details/Question'
import Answer from './details/Answer'


var url = "/api/question/";

var question_app = new Vue({
  el: '#question-detail-app',
  data: {
    results: {},
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
          this.$emit('question-updated-' + question_id, 0);
        } else {
          this.$emit('question-updated-' + question_id, response_files.length);
        }
         this.$emit('answer-updated-' + question_id, response_files)
      }
    }
  },
  mounted: function mounted() {
    this.fetchQuestionData();
  },
  components: {
    'question': Question,
    'answer': Answer
  },
});

Dropzone.options.dropzoneArea = {
  success: function success(file, done) {
    question_app.fetchQuestionData();
  }
};
