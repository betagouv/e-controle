<template>
  <div :id="'dropzone_' + questionId">
    <div v-if="isAudited" class="form-group">
      <div class="form-label">Déposer vos réponses</div>
      <info-bar>
        Astuces : Vous pouvez déposer des dossiers zippés contenant plusieurs documents.
      </info-bar>
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
  import Vue from 'vue'
  import Dropzone from 'dropzone'
  import EventBus from '../events'
  import InfoBar from '../utils/InfoBar'

  import axios from 'axios'

  axios.defaults.xsrfCookieName = 'csrftoken'
  axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
  const url = "/api/question/";

  export default Vue.extend({
    props: [
        'isAudited',
        'questionId'
    ],
    data: function() {
      return {
        faqUrl: '/faq/',
        uploadUrl: '/upload/',
        csrftoken: '',
      }
    },
    components: {
      InfoBar,
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

      Dropzone.options['dropzoneArea' + this.questionId] = {
        success: this.dropzoneSuccessCallback.bind(this)
      }
    },
    methods: {
      dropzoneSuccessCallback: function() {
        this.fetchQuestionData().then(response_files => {
          EventBus.$emit('answer-updated-' + this.questionId, response_files);
          EventBus.$emit('response-file-count-updated-' + this.questionId, response_files.length);
        })
      },
      fetchQuestionData: function () {
        return axios.get(url + this.questionId).then(response =>{
          return response.data.response_files
        });
      },

    }
  })

</script>