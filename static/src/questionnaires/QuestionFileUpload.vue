<template>
<div>
  <input type="file" id="file" ref="file" v-on:change="handleFileUpload()"/>
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
          console.log('SUCCESS!!');
        })
        .catch(function(){
          console.log('FAILURE!!');
        })
      },
      handleFileUpload() {
        this.file = this.$refs.file.files[0]
        this.submitFile()
      }
    }
  })
</script>
