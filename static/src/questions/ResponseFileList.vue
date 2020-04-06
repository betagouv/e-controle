<template>
  <div>
    <success-bar v-if="message" @dismissed="clearMessage"><div v-html="message"></div></success-bar>
    <error-bar v-if="errorMessage" @dismissed="clearErrorMessage"><div v-html="errorMessage"></div></error-bar>
    <div class="table-responsive question-box-child" v-if="files && files.length">
      <div class="form-label">Fichier{{ answer_count===1 ? '': 's' }} déposé{{ answer_count===1 ? '': 's' }}:</div>
      <table class="response-file-list table table-hover table-outline table-vcenter text-nowrap card-table">
        <thead>
          <tr>
            <th style="width: 16%;">Date de dépôt</th>
            <th>Nom du document</th>
            <th style="width: 25%;">Déposant</th>
            <th style="width: 19%;" v-if="isAudited">Mettre à la corbeille</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="file in sortedFiles" :key="file.id">
            <td>
              <div>{{  file.creation_date }}</div>
              <div class="small text-muted">{{  file.creation_time }}</div>
            </td>
            <td>
              <div>
                <a target="_blank" rel="noopener noreferrer" :href="file.url">
                  {{ file.basename }}
                </a>
              </div>
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
      <confirm-modal v-for="file in sortedFiles" :key="file.id"
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

  import Vue from "vue";

  import { clearCache } from '../utils/utils'
  import axios from 'axios'
  import ConfirmModal from '../utils/ConfirmModal'
  import ErrorBar from '../utils/ErrorBar'
  import EventBus from '../events'
  import SuccessBar from '../utils/SuccessBar'
  import VueAxios from 'vue-axios'

  Vue.use(VueAxios, axios)

  axios.defaults.xsrfCookieName = 'csrftoken'
  axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'

  const event_name = 'response-files-updated-'
  const response_file_trash_url = '/api/fichier-reponse/corbeille/'
  const trash_url = '/questionnaire/corbeille/'

  export default Vue.extend({
    data() {
      return {
        files: {},
        errorMessage: '',
        message: '',
      };
    },
    mounted() {
      this.files = this.question.response_files
          .filter(file => !file.is_deleted)

      EventBus.$on(event_name + this.question.id, files => {
        this.files = files.filter(file => !file.is_deleted)
      })
    },
    computed: {
      answer_count: function () {
         return this.files ? this.files.length: 0
      },
      sortedFiles: {
        get: function () {
          return this.files
              .sort((file1, file2) => {
                return (new Date(file1.created).getTime() - new Date(file2.created).getTime())
              })
        },
        set: function (newFiles) {
          this.files = newFiles
        }
      }
    },
    props: {
      question: Object,
      questionnaireId: Number|String,
      isAudited: Boolean,
    },
    methods: {
      sendUpdateEvent: function() {
        EventBus.$emit(event_name + this.question.id, this.files)
      },
      removeFileFromList: function(fileId) {
        const index = this.files.findIndex(file => file.id === fileId)
        const file = this.files[index]
        this.files.splice(index, 1)
        return file
      },
      sendToTrash: function(fileId) {
        this.clearErrorMessage()
        let formData = new FormData()
        formData.append('is_deleted', true)
        this.axios.put(response_file_trash_url + fileId + '/',
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          }
        ).then(response =>{
          console.debug('success deleting response file', response.data)
          clearCache()
          const removedFile = this.removeFileFromList(response.data.id)
          this.sendUpdateEvent()
          this.message = `Le fichier "${removedFile.basename}" a bien été envoyé à la corbeille.
              <a href="${trash_url}${this.questionnaireId}">Cliquez ici</a> pour le voir dans la corbeille.`
        })
        .catch(error => {
          console.error('Error when posting response file', error);
          this.errorMessage = `Le fichier n'a pu être envoyé à la corbeille. Erreur : ${error}`
        })
      },
      clearErrorMessage: function() {
        this.errorMessage = ''
      },
      clearMessage: function() {
        this.message = ''
      },
    },
    components: {
      ConfirmModal,
      ErrorBar,
      SuccessBar,
    }
  });
</script>

<style scoped>

</style>
