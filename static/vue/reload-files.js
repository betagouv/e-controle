const url = "/api/response-file/";

new Vue({
  delimiters: ['[[', ']]'],
  el: '#app',
  data: {
    title: 'Welcome to My Journal',
    results: []
  },
  mounted() {
    axios.get(url).then(response => {
      this.results = response.data
    })
  }
});
