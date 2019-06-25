<template>
<div>
  <label class="btn btn-primary">
    <i class="fe fe-upload mr-2"></i>Ajouter un fichier annexe<input type="file" id="file" ref="file" v-on:change="handleFileUpload()" hidden/>
  </label>
</div>
</template>


<script>
  import axios from 'axios'
  import EventBus from '../events'
  import Vue from "vue"
  import VueAxios from 'vue-axios'

  Vue.use(VueAxios, axios)

  axios.defaults.xsrfCookieName = 'csrftoken'
  axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'

  export default Vue.extend({
    props: {
      questionId: Number
    },
    data () {
      return {
        file: ''
      }
    },
    methods: {
      handleFileUpload() {
        this.file = this.$refs.file.files[0]
        this.submitFile()
      },
      submitFile() {
        if (this.questionId === undefined) {
          console.log('No questionId. We need to save the questionnaire to get an id for this question.')
        }
        let formData = new FormData()
        formData.append('file', this.file)
        formData.append('question', this.questionId)
        this.axios.post('/api/annexe/',
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          }
        ).then(function(){
          // todo send event for individual questions to avoid reloading all questions
          EventBus.$emit('question-files-changed');
        })
        .catch(function(error){
          console.log('Error when posting question file', error);
          EventBus.$emit('display-error', 'L\'annexe n\'a pu être sauvée.')
        })
      }
    }
  })
</script>
