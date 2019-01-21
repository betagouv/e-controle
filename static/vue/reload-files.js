const url = "/api/question/22/";

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
