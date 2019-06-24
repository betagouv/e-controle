<template>
<div class="collapse" :id="'filelist' + (themeIndex + 1) + (qIndex + 1)">
  <div>
    <div class="card card-body">
      <div v-if="files && files.length">
        <div v-if="files.length > 1">Fichiers annexes à la question:</div>
        <div v-else>Fichier annexe à la question:</div>
        <ul>
          <li v-for="(file, index) in files" :key="index">
            <a :href="file.url">{{ file.basename }}</a>
          </li>
        </ul>
      </div>
      <question-file-upload :question-id="questionId"></question-file-upload>
    </div>
  </div>
</div>

</template>


<script>
  import axios from 'axios'
  import EventBus from '../events'
  import QuestionFileUpload from "./QuestionFileUpload"
  import Vue from "vue"
  import VueAxios from 'vue-axios'

  Vue.use(VueAxios, axios)

  export default Vue.extend({
    props: {
      questionId: Number,
      qIndex: Number,
      themeIndex: Number
    },
    data() {
      return {
        files: []
      }
    },
    components: {
      QuestionFileUpload
    },
    methods: {
      getFiles() {
        Vue.axios.get('/api/annexe/', {
          params: {
            question: this.questionId
          }
        }).then((response) => {
          this.files = response.data
          console.log(this.files)
        })
      }
    },
    mounted() {
      EventBus.$on('question-files-changed', data => {
        this.getFiles()
      })
    }
  })
</script>
