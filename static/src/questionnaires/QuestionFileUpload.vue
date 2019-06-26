<template>
<div>
  <div v-if="questionId">
    <label class="btn btn-primary" >
      <i class="fe fe-upload mr-2" ></i>Ajouter un fichier annexe<input type="file" id="file" ref="file" v-on:change="handleFileUpload()" hidden/>
    </label>
  </div>
  <div v-else>
    <label class="btn btn-primary disabled" >
      <i class="fe fe-upload mr-2" ></i>Ajouter un fichier annexe
    </label>
    <div class="small">Pour pouvoir ajouter des annexes, vous devez d'abord enregistrer votre brouillon.</div>
  </div>
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
