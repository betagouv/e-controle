<template>
  <div>
    <questionnaire-metadata :questionnaire="questionnaire">
    </questionnaire-metadata>

    <div id="body" class="row row-cards">
      <div id="sidebar" class="col-lg-4">
        <div class="row sticky">
          <div class="col-md-6 col-lg-12">
            <div class="card">
              <div class="card-header bg-blue text-white">
                <h4 class="card-title">Thèmes</h4>
              </div>
              <table class="table card-table">
                <tbody>
                <tr v-for="(theme, themeIndex) in questionnaire.themes" class="theme-row">
                  <td>
                    <a v-bind:href="'#theme' + (themeIndex + 1)">
                      {{ themeIndex + 1 }}. {{ theme.title }}
                    </a>
                  </td>
                </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <div class="col-lg-8">
        <div v-bind:id="'theme' + (themeIndex + 1)"
             v-for="(theme, themeIndex) in questionnaire.themes"
             class="card">
          <div class="card-status card-status-top bg-blue"></div>
          <div class="card-header">
            <h3 class="card-title">{{ themeIndex + 1 }}. {{ theme.title }}</h3>
          </div>

          <question-box v-for="(question, qIndex) in theme.questions"
                        :theme-numbering="themeIndex + 1"
                        :question-numbering="qIndex + 1"
                        :question="question">
            <question-file-list :question-id="question.id" :with-delete="false"></question-file-list>
            <response-file-list :question_id="question.id"></response-file-list>
            <response-dropzone :is-audited="user.is_audited"
                               :question-id="question.id">
            </response-dropzone>
          </question-box>

        </div>
      </div>

    </div>
  </div>

</template>

<script>
  import Vue from "vue";

  import axios from 'axios'
  import QuestionBox from '../questions/QuestionBox'
  import QuestionFileList from '../questions/QuestionFileList'
  import QuestionnaireMetadata from './QuestionnaireMetadata'
  import ResponseDropzone from '../questions/ResponseDropzone'
  import ResponseFileList from '../questions/ResponseFileList'

  const questionnaire_url = "/api/questionnaire/";
  const session_user_url = "/api/user/current/";

  export default Vue.extend({
    props: [ 'questionnaireId' ],
    data : function () {
      return {
        questionnaire: '',
        user: '',
      }
    },
    mounted: function(){
      this.getQuestionnaire()
      this.getSessionUser()
    },
    methods: {
      getQuestionnaire: function() {
        axios.get(questionnaire_url + this.questionnaireId).then(response => {
          this.questionnaire = response.data
        });
      },
      // todo reuse the Vuex store ?
      getSessionUser: function() {
        axios.get(session_user_url).then(response => {
          this.user = response.data
        })
      },
    },
    components: {
      QuestionBox,
      QuestionFileList,
      QuestionnaireMetadata,
      ResponseDropzone,
      ResponseFileList,
    }
  })

</script>