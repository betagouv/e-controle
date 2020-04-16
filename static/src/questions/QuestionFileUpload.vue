<template>
<div>
  <error-bar v-if="errorMessage" @dismissed="clearError">
    {{ errorMessage }}
  </error-bar>
  <div v-if="question.id">
    <label class="btn btn-primary">
      <i class="fe fe-upload mr-2"></i>
      Ajouter un fichier annexe
      <input type="file" ref="fileInput" v-on:change="handleFileUpload()" hidden/>
    </label>
  </div>
  <div v-else>
    <label class="btn btn-primary disabled" >
      <i class="fe fe-upload mr-2" ></i>
      Ajouter un fichier annexe
    </label>
    <div class="small">
      Pour pouvoir ajouter des annexes,
    </div>
    <div class="small">
      vous devez d'abord enregistrer
    </div>
    <div class="small">
      votre brouillon.
    </div>
  </div>
</div>
</template>

<script>
import axios from 'axios'
import backendUrls from '../utils/backend'
import ErrorBar from '../utils/ErrorBar'
import EventBus from '../events'
import Vue from 'vue'

export default Vue.extend({
  props: {
    question: Object,
  },
  data () {
    return {
      errorMessage: undefined,
      file: '',
    }
  },
  components: {
    ErrorBar,
  },
  methods: {
    clearError() {
      this.errorMessage = undefined
    },
    handleFileUpload() {
      this.file = this.$refs.fileInput.files[0]
      this.submitFile()
    },
    submitFile() {
      this.clearError()
      const formData = new FormData()
      formData.append('file', this.file)
      formData.append('question', this.question.id)
      axios.post(
        backendUrls.annexe(),
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })
        .then(response => {
          console.debug('QuestionFileUpload response', response)
          const newFile = response.data
          this.question.question_files.push(newFile)
        })
        .catch(error => {
          console.log('Error when posting question file', error)
          this.errorMessage = 'L\'annexe n\'a pu être sauvée.'
        })
    },
  },
})
</script>
