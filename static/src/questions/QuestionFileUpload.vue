<template>
<div>
  <div v-if="questionId">
    <label class="btn btn-primary">
      <i class="fe fe-upload mr-2"></i>
      Ajouter un fichier annexe
      <input type="file" id="file" ref="file" v-on:change="handleFileUpload()" hidden/>
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
import EventBus from '../events'
import Vue from 'vue'

export default Vue.extend({
  props: {
    questionId: Number,
  },
  data () {
    return {
      file: '',
    }
  },
  methods: {
    handleFileUpload() {
      this.file = this.$refs.file.files[0]
      this.submitFile()
    },
    submitFile() {
      const formData = new FormData()
      formData.append('file', this.file)
      formData.append('question', this.questionId)
      axios.post(
        backendUrls.annexe(),
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })
        .then(function(response) {
          console.debug('QuestionFileUpload response', response)
          EventBus.$emit('question-file-added', response.data)
        })
        .catch(function(error) {
          console.log('Error when posting question file', error)
          EventBus.$emit('display-error', 'L\'annexe n\'a pu être sauvée.')
        })
    },
  },
})
</script>
