<template>
  <div>
    <div>
      <div class="card card-body">
        <div v-if="files && files.length">
          <div v-if="files.length > 1">Fichiers annexes à la question:</div>
          <div v-else>Fichier annexe à la question:</div>
          <ul>
            <li v-for="(file, index) in files" :key="index">
              <a :href="file.url">{{ file.basename }}</a>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>

</template>


<script>
  import axios from 'axios'
  import EventBus from '../events'
  import Vue from "vue"
  import VueAxios from 'vue-axios'

  Vue.use(VueAxios, axios)

  export default Vue.extend({
    props: {
      questionId: Number,
      qIndex: Number,
      themeIndex: Number
    },
    data() {
      return {
        files: []
      }
    },
    methods: {
      getFiles() {
        Vue.axios.get('/api/annexe/', {
          params: {
            // Todo on first load, the questionId is not found so all files are fetched.
            question: this.questionId
          }
        }).then((response) => {
          this.files = response.data
          console.log(this.files)
        })
      }
    },
    mounted() {
      EventBus.$on('question-files-changed', () => {
        this.getFiles()
      })
    }
  })
</script>
