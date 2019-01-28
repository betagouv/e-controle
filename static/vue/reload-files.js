const url = "/api/question/"
const url_comment = "/api/comment/"


Vue.component('text-comment', {
  props: ['text', 'questionid'],
  template: '<p>{{ text }} + {{ questionid }}</p>'
})

var question_app = new Vue({
  delimiters: ['[[', ']]'],
  el: '#question-detail-app',
  data: {
    results: {response_files: {}},
    r_files: {},
    comments: [
      {text: 'test'}
    ]
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


/*var comment_app = new Vue({
  delimiters: ['[[', ']]'],
  el: '#comment-app',
  data: {
    comments: {}
  },
  methods: {
    fetchCommentData() {
      axios.get(url).then(response => {
        this.results = response.data

      })
    },
    saveComment(comment_data) {
      for (question_id in comment_data) {
        comments = comment_data[question_id].comments
        if (comments.length == 0) {
          comments = null
        }
        this.r_comments[question_id] = comments
      }
    }
  },
  mounted: function () {
    this.fetchCommentData()
  }
})
*/
Dropzone.options.dropzoneArea = {
  success: function(file, done) {
    question_app.fetchQuestionData()
  }
}
