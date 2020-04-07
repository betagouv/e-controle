<template>
  <div>
    <success-bar v-if="hasSucessMessage" @dismissed="clearSuccessMessage">
      Le fichier "{{ successFilename }}" a bien été envoyé à la corbeille.
      <a :href="trashUrl">Cliquez ici</a>
      pour le voir dans la corbeille.
    </success-bar>
    <error-bar v-if="errorMessage" @dismissed="clearErrorMessage">
      {{ errorMessage }}
    </error-bar>
    <div class="table-responsive question-box-child" v-if="files && files.length">
      <div class="form-label">
        Fichier{{ answer_count===1 ? '': 's' }} déposé{{ answer_count===1 ? '': 's' }}:
      </div>
      <table class="response-file-list table table-hover table-outline table-vcenter text-nowrap
                    card-table">
        <thead>
          <tr>
            <th style="width: 16%;">Date de dépôt</th>
            <th>Nom du document</th>
            <th style="width: 25%;">Déposant</th>
            <th style="width: 19%;" v-if="isAudited">Mettre à la corbeille</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="file in files" :key="file.id">
            <td>
              <div>{{  file.creation_date }}</div>
              <div class="small text-muted">{{  file.creation_time }}</div>
            </td>
            <td>
              <div><a target="_blank" :href="file.url">{{ file.basename }}</a></div>
            </td>
            <td>
              <div>{{ file.author.first_name }} {{ file.author.last_name }}</div>
            </td>
            <td v-if="isAudited">
              <a href="javascript:void(0)"
                 data-toggle="modal"
                 :data-target="'#trash-confirm-modal-' + file.id"
                 class="fe fe-trash-2 btn btn-outline-primary"
              >
              </a>
            </td>
          </tr>
        </tbody>
      </table>
      <confirm-modal v-for="file in files" :key="file.id"
                     :id="'trash-confirm-modal-' + file.id"
                     title="Corbeille"
                     confirm-button="Oui, envoyer à la corbeille"
                     cancel-button="Non, annuler"
                     @confirm="sendToTrash(file.id)"
      >
        <p>
          Vous allez envoyer “{{ file.basename }}” à la corbeille.
        </p>
      </confirm-modal>
    </div>
  </div>
</template>

<script>

import Vue from 'vue'

import axios from 'axios'
import backendUrls from '../utils/backend'
import { clearCache } from '../utils/utils'
import ConfirmModal from '../utils/ConfirmModal'
import ErrorBar from '../utils/ErrorBar'
import EventBus from '../events'
import SuccessBar from '../utils/SuccessBar'
import VueAxios from 'vue-axios'

Vue.use(VueAxios, axios)

axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'

const EVENT_NAME = 'response-files-updated-'

export default Vue.extend({
  props: {
    question: Object,
    questionnaireId: Number,
    isAudited: Boolean,
  },
  data() {
    return {
      files: {},
      errorMessage: '',
      hasSucessMessage: false,
      successFilename: '',
    }
  },
  mounted() {
    const makeDisplayFileList = files => {
      return files.filter(file => !file.is_deleted)
        .sort((file1, file2) => {
          return (new Date(file1.created).getTime() - new Date(file2.created).getTime())
        })
    }

    this.files = makeDisplayFileList(this.question.response_files)

    // When we get a new list of files, replace the old one
    EventBus.$on(EVENT_NAME + this.question.id, files => {
      this.files = makeDisplayFileList(files)
    })
  },
  computed: {
    answer_count: function () {
      return this.files ? this.files.length : 0
    },
    trashUrl() {
      return backendUrls.trash(this.questionnaireId)
    },
  },
  methods: {
    sendUpdateEvent: function() {
      EventBus.$emit(EVENT_NAME + this.question.id, this.files)
    },
    removeFileFromList: function(fileId) {
      const index = this.files.findIndex(file => file.id === fileId)
      const file = this.files[index]
      this.files.splice(index, 1)
      return file
    },
    sendToTrash: function(fileId) {
      this.clearErrorMessage()
      this.clearSuccessMessage()
      const formData = new FormData()
      formData.append('is_deleted', true)
      this.axios.put(backendUrls.responseFileTrash(fileId),
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        },
      ).then(response => {
        console.debug('success deleting response file', response.data)
        clearCache()
        const removedFile = this.removeFileFromList(response.data.id)
        this.sendUpdateEvent()
        this.displaySucessMessage(removedFile.basename)
      })
        .catch(error => {
          console.error('Error when posting response file', error)
          this.errorMessage = `Le fichier n'a pu être envoyé à la corbeille. Erreur : ${error}`
        })
    },
    clearErrorMessage: function() {
      this.errorMessage = ''
    },
    displaySucessMessage(successFilename) {
      this.hasSucessMessage = true
      this.successFilename = successFilename
    },
    clearSuccessMessage: function() {
      this.hasSucessMessage = false
      this.successFilename = ''
    },
  },
  components: {
    ConfirmModal,
    ErrorBar,
    SuccessBar,
  },
})
</script>

<style scoped>

</style>
