<template>
  <span>
    <a href="javascript:void(0)" @click.prevent="deleteFile(questionFileId)" class="btn btn-link" title="Supprimer le fichier">
      <i class="fe fe-trash-2"></i>
    </a>
  </span>
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
      questionFileId: Number
    },
    methods: {
      deleteFile() {
        this.axios.delete('/api/annexe/' + this.questionFileId).then(function(){
          EventBus.$emit('question-files-changed');
        })
        .catch(function(error){
          console.log('Error when deleting question file', error);
          EventBus.$emit('display-error', 'Le fichier n\'a pu être supprimé.')
        })
      }
    }
  })
</script>
