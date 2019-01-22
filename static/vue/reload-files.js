const url = "/api/question/"

var app = new Vue({
  delimiters: ['[[', ']]'],
  el: '#app',
  data: {
    title: 'Welcome to My Journal',
    results: {}
  },
  mounted() {
    axios.get(url).then(response => {
      this.results = response.data
    })
  }
});
