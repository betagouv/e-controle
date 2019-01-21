new Vue({
  delimiters: ['[[', ']]'],
  el: '#app',
  data: {
    title: 'Welcome to My Journal',
    results: []
  },
  mounted() {
		const url = this.$refs.app.dataset.url;
    axios.get(url).then(response => {
      this.results = response.data
    })
  }
});
