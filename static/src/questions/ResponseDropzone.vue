<template>
  <div :id="'dropzone_' + questionId">
    <div v-show="isAudited" class="form-group question-box-child">
      <div class="form-label">Déposer vos réponses</div>
      <info-bar>
        Astuces : Vous pouvez déposer des dossiers zippés contenant plusieurs documents.
      </info-bar>
      <error-bar v-if="hasErrors">
        <div>
          Le fichier déposé n'a pas pu être transmis.
        </div>
      </error-bar>
      <form class="dropzone" :action="uploadUrl" method="post" enctype="multipart/form-data" :id="'dropzone-area-' + questionId ">
        <input type="hidden" name="csrfmiddlewaretoken" :value="csrftoken">
        <div class="dz-message" data-dz-message><span>Cliquer ou glisser-déposer vos fichiers ou dossiers zippés.</span></div>
        <input type="hidden" id="idQuestionId" name="question_id" :value="questionId" />
        <div class="fallback">
          <input name="file" type="file" multiple />
        </div>
      </form>
      <div class="text-right">
        <i class="dropdown-icon fe fe-help-circle"></i><a :href="faqUrl">Des questions sur le dépôt de fichiers ?</a>
      </div>
    </div>
  </div>

</template>

<script>
  import { clearCache } from '../utils/utils'
  import Dropzone from 'dropzone'
  import ErrorBar from "../utils/ErrorBar"
  import EventBus from '../events'
  import InfoBar from '../utils/InfoBar'
  import Vue from 'vue'

  import axios from 'axios'

  axios.defaults.xsrfCookieName = 'csrftoken'
  axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
  const url = "/api/question/";

  export default Vue.extend({
    props: [
        // Note : this field will change because the user object is fetched from server and arrives late.
        // This can break the rendering of the dropbox, it cannot be rendered late.
        // So we use a v-show in the template, rather than a v-if, to render early.
        'isAudited',
        'questionId'
    ],
    data: function() {
      return {
        faqUrl: '/faq/',
        uploadUrl: '/upload/',
        csrftoken: '',
        hasErrors: false
      }
    },
    components: {
      InfoBar,
      ErrorBar
    },
    mounted: function(){
      // Weird function copied from w3schools
      function readCookie(name) {
        var nameEQ = name + "=";
        var ca = document.cookie.split(';');
        for(var i=0;i < ca.length;i++) {
            var c = ca[i];
            while (c.charAt(0) === ' ') {
                c = c.substring(1,c.length);
            }
            if (c.indexOf(nameEQ) === 0) {
                return c.substring(nameEQ.length,c.length);
            }
        }
        return null;
      }

      this.csrftoken = readCookie('csrftoken')

      const errorCallback = this.dropzoneErrorCallback.bind(this)
      const successCallback = this.dropzoneSuccessCallback.bind(this)

      Dropzone.options['dropzoneArea' + this.questionId] = {
        init: function() {
          this.on('success', file => {
            successCallback()
            // Remove thumbnail for successful upload (we already have a file list for confirmation)
            this.removeFile(file)
          })
          this.on('error', errorCallback)
        }
      }
    },
    methods: {
      clearErrors() {
        this.hasErrors = false
      },
      dropzoneSuccessCallback: function() {
        clearCache()
        this.fetchQuestionData().then(response_files => {
          EventBus.$emit('response-files-updated-' + this.questionId, response_files);
        })
      },
      dropzoneErrorCallback: function(error, errorMessage) {
        clearCache()
        this.hasErrors = true
        console.debug("Error when uploading response file", errorMessage.error)
        // Todo : afficher les erreurs serveur (errorMessage.error) pour differencier les cas
        //  (fichier vide, fichier trop gros, autre)
      },
      fetchQuestionData: function () {
        this.clearErrors()
        return axios.get(url + this.questionId).then(response =>{
          return response.data.response_files
        });
      },

    }
  })

</script>
