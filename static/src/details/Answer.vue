<template>
  <div :id="'answer_' + questionId" class="card-body">
    <answer-file-list :question_id="questionId"></answer-file-list>
    cookies {{ cookies }} cookie {{ cookie}}
    <div v-if="isAudited" class="form-group">
      <div class="form-label">Déposer vos réponses</div>
      <info-bar>
        Astuces : Vous pouvez déposer des dossiers zippés contenant plusieurs documents.
      </info-bar>
      <form class="dropzone" :action="uploadUrl" method="post" enctype="multipart/form-data" :id="'dropzone-area-' + questionId ">
        <input type="hidden" name="csrfmiddlewaretoken" :value="cookie">
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
  import AnswerFileList from './AnswerFileList'
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
        cookie: 'not found',
        cookies: document.cookie,
      }
    },
    components: {
      AnswerFileList,
      InfoBar,
    },
    mounted: function(){
      function getCookie(cookieName) {
//        console.log(document.cookie)
        const decodedCookie = decodeURIComponent(document.cookie)
//        console.log(decodedCookie)
        const cookies = decodedCookie.split(';')
        cookies.forEach((cookie) => {
 //         console.log('cookie', cookie)
          const keyValue = cookie.split('=')
   //       console.log('keyValue', keyValue)
     //     console.log('keyValue[0].trim()', keyValue[0].trim())
       //   console.log('cookieName', cookieName)
         // console.log('equals', keyValue[0].trim() === cookieName)
          if (keyValue[0].trim() === cookieName) {
           // console.log('keyValue[1]', keyValue[1])
            return keyValue[1].trim() // why no return here???
          }
        })
      }

      this.cookie = getCookie('csrftoken')
      this.cookie = '5MNNGDOe99seeOD1AGAr0gIy78TqqUgnY5zmUxhvaW8YIoUlFKeTSuA9AoXn8ENK'

      Dropzone.options['dropzoneArea' + this.questionId] = {
        success: this.dropzoneSuccessCallback.bind(this)
      }
    },
    methods: {
      dropzoneSuccessCallback: function() {
        this.fetchQuestionData().then(response_files => {
          EventBus.$emit('answer-updated-' + this.questionId, response_files);
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