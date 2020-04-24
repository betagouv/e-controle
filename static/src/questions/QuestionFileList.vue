<template>
  <div>
    <error-bar v-if="errorMessage" @dismissed="clearError">
      {{ errorMessage }}
    </error-bar>
    <div v-if="files && files.length" class="question-box-child">
      <div v-if="files.length > 1" class="form-label">Fichiers annexes à la question:</div>
      <div v-else class="form-label">Fichier annexe à la question:</div>
      <ul>
        <li v-for="(file, index) in files"
            :key="index"
            class="question-file">
          <a :href="file.url">
            {{ file.basename }}
          </a>
          <span v-if="withDelete">
            <button @click.prevent="deleteFile(file.id)"
                    class="btn btn-link"
                    title="Supprimer le fichier">
              <i class="fe fe-trash-2"></i>
            </button>
          </span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import backendUrls from '../utils/backend'
import ErrorBar from '../utils/ErrorBar'
import Vue from 'vue'

export default Vue.extend({
  props: {
    files: Array,
    withDelete: Boolean,
  },
  data() {
    return {
      errorMessage: undefined,
    }
  },
  components: {
    ErrorBar,
  },
  methods: {
    clearError() {
      this.errorMessage = undefined
    },
    deleteFileFromVuex(fileId) {
      for (let i = 0; i < this.files.length; i++) {
        if (this.files[i].id === fileId) {
          this.files.splice(i, 1)
          console.debug('Deleted file', fileId, 'from vuex')
        }
      }
    },
    deleteFile(fileId) {
      this.clearError()
      axios.delete(backendUrls.annexe(fileId))
        .then(() => {
          this.deleteFileFromVuex(fileId)
        })
        .catch((error) => {
          console.log('Error when deleting question file', error)
          this.errorMessage = 'Le fichier n\'a pu être supprimé.'
        })
    },
  },
})
</script>
