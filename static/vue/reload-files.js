const url = "/api/question/"

var app = new Vue({
  delimiters: ['[[', ']]'],
  el: '#app',
  data: {
    title: 'Welcome to My Journal',
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
    app.fetchQuestionData()
  }
};
