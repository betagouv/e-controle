<template>
  <div v-if="files && files.length" class="question-box-child">
    <div v-if="files.length > 1" class="form-label">Fichiers annexes à la question:</div>
    <div v-else class="form-label">Fichier annexe à la question:</div>
    <ul>
      <li v-for="(file, index) in files" :key="index">
        <a :href="file.url">{{ file.basename }}</a>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios'
import backendUrls from '../utils/backend'
import EventBus from '../events'
import Vue from 'vue'

export default Vue.extend({
  props: {
    questionId: Number | String,
    questionNumber: String,
  },
  data() {
    return {
      files: [],
    }
  },
  methods: {
    getFiles() {
      if (this.questionId === undefined) {
        console.debug(
          'No questionId for question', this.questionNumber, ', so cannot fetch file list.')
        return
      }
      axios.get(backendUrls.annexe(), {
        params: {
          question: this.questionId,
        },
      }).then((response) => {
        this.files = response.data
        EventBus.$emit('question-file-count-changed-' + this.questionId, this.files.length)
      })
    },
  },
  mounted() {
    this.getFiles()
  },
})
</script>
