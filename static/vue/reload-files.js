const url = "/api/question/"

var question_app = new Vue({
  delimiters: ['[[', ']]'],
  el: '#question-detail-app',
  data: {
    results: {},
    r_files: {}
  },
  methods: {
		fetchQuestionData() {
      axios.get(url).then(response => {
        this.results = response.data
        this.saveResponseFiles(response.data)
      })
    },
    saveResponseFiles(question_data) {
      for (question_id in question_data) {
        response_files = question_data[question_id].response_files
        if (response_files.length == 0) {
          response_files = null
        }
        this.r_files[question_id] = response_files
      }
    }
  },
  mounted: function () {
  		this.fetchQuestionData()
  	}
})

Dropzone.options.dropzoneArea = {
  success: function(file, done) {
    question_app.fetchQuestionData()
  }
}
