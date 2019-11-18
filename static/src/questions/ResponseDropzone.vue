<template>
  <div :id="'dropzone_' + questionId" class="response-dropzone">
    <div v-show="isAudited" class="form-group question-box-child">
      <div class="form-label">Déposer vos réponses</div>
      <error-bar v-if="hasErrors" @dismissed="clearErrors">
        <div>
          Une erreur s'est produite lors de la transmision d'un fichier.
        </div>
      </error-bar>
      <form class="dropzone" :action="uploadUrl" method="post" enctype="multipart/form-data" :id="'dropzone-area-' + questionId ">
        <input type="hidden" name="csrfmiddlewaretoken" :value="csrftoken">
        <div class="dz-message" data-dz-message><span>Cliquer ou glisser-déposer vos fichiers.</span></div>
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
  const url = "/api/question/"
  const UPLOAD_TIMEOUT_MS = 3 * 60 * 1000 // 3 min : timeout apache

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
        errorMessage: "",
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
      const addedFileCallback = this.clearErrors.bind(this)
      const timeoutCallback = this.dropzoneTimeoutCallback.bind(this)

      Dropzone.options['dropzoneArea' + this.questionId] = {
        addRemoveLinks: true,
        timeout: UPLOAD_TIMEOUT_MS,
        init: function() {
          this.on('success', successCallback),
          this.on('error', errorCallback),
          this.on('addedfile', addedFileCallback)
          this.on('sending', (file, xhr, formdata) => {
            console.debug('dropzone sending', file, xhr, formdata)
            xhr.ontimeout = error => {
              timeoutCallback(file, error)
            }
          })
        },
        dictCancelUpload: "Annuler l'envoi",
        dictUploadCanceled: "L'envoi a été annulé.",
        dictCancelUploadConfirmation: "Etes-vous sûr.e de vouloir annuler l'envoi?",
        dictRemoveFile: "Retirer le fichier",
        dictFileTooBig: "La taille du fichier dépasse la limite authorisée de {{maxFilesize}}Mo."
      }
    },
    methods: {
      clearErrors() {
        this.errors = ""
        this.hasErrors = false
      },
      styleSuccess(file) {
        file.previewElement.getElementsByClassName('dz-success-mark')[0]
            .getElementsByTagName('g')[0]
            .getElementsByTagName('path')[0]
            .setAttribute('fill', '#5EBB00') // success color in tabler
        file.previewElement.getElementsByClassName('dz-remove')[0].remove()
      },
      styleError(file) {
        file.previewElement.getElementsByClassName('dz-error-mark')[0]
            .getElementsByTagName('g')[0]
            .getElementsByTagName('g')[0]
            .setAttribute('fill', '#cd201f') // danger color in tabler
        file.previewElement.getElementsByClassName('dz-remove')[0].remove()
      },
      styleTimeout(file, errorMessage) {
        // Dropzone leaves the file in "processing" state, which looks weird. We style it to look like an error state.
        file.previewElement.classList.add('dz-error')
        file.previewElement.classList.remove('dz-procession')
        file.previewElement.getElementsByClassName('dz-progress')[0].remove()
        file.previewElement.getElementsByClassName('dz-error-message')[0]
            .getElementsByTagName('span')[0].textContent = errorMessage
        this.styleError(file)
      },
      dropzoneTimeoutCallback: function(file, error) {
        console.debug('dropzone timeout', file, error)
        clearCache()

        this.hasErrors = true
        this.errorMessage = 'L\'envoi du fichier "' + file.name + '" a mis plus de ' + (UPLOAD_TIMEOUT_MS / 1000) +
            ' secondes, et a été annulé. Essayez avec des fichiers plus petits, ou un réseau internet plus rapide.'

        this.styleTimeout(file, this.errorMessage)
      },
      dropzoneSuccessCallback: function(file) {
        clearCache()
        this.styleSuccess(file)
        this.fetchQuestionData().then(response_files => {
          EventBus.$emit('response-files-updated-' + this.questionId, response_files);
        })
      },
      dropzoneErrorCallback: function(file, errorMessage) {
        clearCache()
        if (file.status !== 'canceled') {
          this.hasErrors = true
          this.errorMessage =  errorMessage
        }
        this.styleError(file)
        console.debug("Error when uploading response file.", file, errorMessage)
      },
      fetchQuestionData: function () {
        return axios.get(url + this.questionId).then(response =>{
          return response.data.response_files
        });
      },

    }
  })

</script>

<style>
  /* Shift the error bubble down, it's overlapping the "Remove file" link. */
  .response-dropzone .dropzone .dz-preview .dz-error-message {
    top:150px;
  }

  /* The progress bar and success/error mark are on top of the filename. Move it up. */
  .dropzone .dz-preview .dz-details {
    padding-top: 0.7em;
  }
  .dropzone .dz-preview .dz-details .dz-size {
    margin-bottom: 0.3em;
  }
  .dropzone .dz-preview .dz-success-mark, .dropzone .dz-preview .dz-error-mark {
    top: 60%;
  }

  /* 
    Make the checkmark for success stay visible, instead of disappearing after a while.
    We just copy the animation for the error case.
  */
  .response-dropzone .dropzone .dz-preview.dz-success .dz-success-mark {
    opacity: 1;
    -webkit-animation: slide-in 3s cubic-bezier(0.77, 0, 0.175, 1);
    -moz-animation: slide-in 3s cubic-bezier(0.77, 0, 0.175, 1);
    -ms-animation: slide-in 3s cubic-bezier(0.77, 0, 0.175, 1);
    -o-animation: slide-in 3s cubic-bezier(0.77, 0, 0.175, 1);
    animation: slide-in 3s cubic-bezier(0.77, 0, 0.175, 1); 
  }
</style>