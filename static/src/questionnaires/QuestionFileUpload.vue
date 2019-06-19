<template>
    <div>
      <input type="file" id="file" ref="file" v-on:change="handleFileUpload()"/>
  </div>
</template>


<script>
  import Vue from "vue"
  import axios from 'axios'
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
        this.axios.post('/api/annexe/',
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          }
        ).then(function(){
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
