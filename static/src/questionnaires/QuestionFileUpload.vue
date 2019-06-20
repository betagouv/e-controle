<template>
<div>
  <label class="btn btn-primary">
    <i class="fe fe-upload mr-2"></i>Fichier Annexe<input type="file" id="file" ref="file" v-on:change="handleFileUpload()" hidden/>
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
          EventBus.$emit('question-files-changed');
        })
        .catch(function(){
          console.log('Error when posting question file');
        })
      }
    }
  })
</script>
