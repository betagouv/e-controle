<template>
<div v-if="files && files.length">
  <ul>
    <li v-for="(file, index) in files" :key="index">
      <a :href="file.url">{{ file.basename }}</a>
    </li>
  </ul>
</div>
</template>


<script>
  import axios from 'axios'
  import EventBus from '../events'
  import Vue from "vue"
  import VueAxios from 'vue-axios'

  Vue.use(VueAxios, axios)

  export default Vue.extend({
    props: {
      questionId: Number
    },
    data() {
      return {
        files: []
      }
    },
    methods: {
      getFiles() {
        console.log('LIST ' + this.questionId)
        Vue.axios.get('/api/annexe/', {
          params: {
            question: this.questionId
          }
        }).then((response) => {
          this.files = response.data
        })
      }
    },
    mounted() {
      this.getFiles()
      EventBus.$on('question-files-changed', data => {
        this.getFiles()
      })
    }
  })
</script>
