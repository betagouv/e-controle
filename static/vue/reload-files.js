const url = "/api/question/"

var question_app = new Vue({
  delimiters: ['[[', ']]'],
  el: '#question-detail-app',
  data: {
    results: {}
  },
  methods: {
		fetchQuestionData() {
      axios.get(url).then(response => {
        this.results = response.data
      })
    }
  },
  mounted: function () {
  		this.fetchQuestionData();
  	}
});

Dropzone.options.dropzoneArea = {
  success: function(file, done) {
    question_app.fetchQuestionData()
  }
};
