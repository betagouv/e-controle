const url = "/api/question/"
const url_comment = "/api/comment/"

/*Vue.filter('first', function (value) {
  return value.charAt(0)
})*/

Vue.component('text-comment', {
  props: ['text', 'questionid', 'date', 'firstname', 'lastname'],
  template: `<div class="media">
                <div class="media-body">
                  <div class="media-heading">
                  <small class="float-right text-muted">{{ date }}</small>
                  <h5> {{ firstname }} {{ lastname }}</h5>
                  </div>
                  <div>
                    {{ text }}
                  </div>
                </div>
            </div>`,
})

Vue.component('button-comment', {
  props: ['questionid', 'userid'],
  data: function() {
    return {text: ''}
  },
  template: `<div>
              <textarea class="form-control" name="example-textarea-input" rows="4" placeholder="" v-model="text"></textarea> 
              <div class="text-right">
                <button class="btn btn-primary center" v-on:click=addComment>
                  Envoyer
                </button>
              </div>
            </div>`,
  methods: {
    addComment() {
      var vm = this
      vm.$parent.postComment(vm._props.questionid, vm._props.userid, vm.text)
      vm.text = ''
    }
  },
  mounted: function() {
    var vm = this
    vm.$parent.getCommentByQuestionId(vm._props.questionid)
  }
})

var question_app = new Vue({
  delimiters: ['[[', ']]'],
  el: '#question-detail-app',
  data: {
    results: {response_files: {}},
    r_files: {},
    comments: {}
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
    },
    getCommentByQuestionId(question_id) {
      url_by_id = url_comment + "?questionid=" + question_id
      axios.get(url_by_id).then(response => {
        this.comments[question_id] = []
        this.comments[question_id].push(response.data)
      }).catch(error => {
          console.log(error)
      })
    },
    postComment(questionid, author_id, text) {
      // Code to get token from cookie
      var cookiestring = RegExp(""+"csrftoken"+"[^;]+").exec(document.cookie);
      csrftoken = decodeURIComponent(!!cookiestring ? cookiestring.toString().replace(/^[^=]+./,"") : "");
      axios.post(url_comment,
        {
          question: questionid,
          author_id: author_id,
          text: text,
        },
        {
          headers : {
            "X-CSRFToken": csrftoken 
          }
        }
      ).then(response => {
        this.comments[questionid][0].push(response.data)
        this.$forceUpdate();
      })
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
