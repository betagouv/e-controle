<template>
  <div v-if="files && files.length" class="border-0">
    <div v-if="files.length > 1" class="form-label">Fichiers annexes à la question:</div>
    <div v-else class="form-label">Fichier annexe à la question:</div>
    <ul>
      <li v-for="(file, index) in files" :key="index">
        <a :href="file.url">{{ file.basename }}</a>
          <question-file-delete v-if="withDelete" :question-file-id="file.id"></question-file-delete>
      </li>
    </ul>
  </div>
</template>


<script>
  import axios from 'axios'
  import EventBus from '../events'
  import QuestionFileDelete from "./QuestionFileDelete"
  import Vue from "vue"
  import VueAxios from 'vue-axios'

  Vue.use(VueAxios, axios)

  export default Vue.extend({
    props: {
      questionId: Number | String,
      questionNumber: String,
      withDelete: {
        type: Boolean,
        default: true
      }
    },
    data() {
      return {
        files: []
      }
    },
    components: {
      QuestionFileDelete
    },
    methods: {
      getFiles() {
        if (this.questionId === undefined) {
          console.debug('No questionId for question', this.questionNumber, ', so cannot fetch file list.')
          return
        }
        Vue.axios.get('/api/annexe/', {
          params: {
            question: this.questionId
          }
        }).then((response) => {
          this.files = response.data
          EventBus.$emit('question-file-count-changed-' + this.questionId, this.files.length)
        })
      }
    },
    mounted() {
      EventBus.$on('question-files-changed', () => {
        this.getFiles()
      })
      this.getFiles()
    }
  })
</script>
