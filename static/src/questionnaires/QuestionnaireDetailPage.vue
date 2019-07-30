<template>
  <div>
    <questionnaire-metadata :questionnaire="questionnaire">
    </questionnaire-metadata>

    <div id="body" class="row row-cards">
      <div id="sidebar" class="col-lg-4">
        <theme-list-sidebar :themes="questionnaire.themes">
        </theme-list-sidebar>
        <div><a :href="'/questionnaire/corbeille/' "><i class="fe fe-trash-2 mr-1"></i>Corbeille</a></div>
      </div>

      <div class="col-lg-8">
        <theme-box v-for="(theme, themeIndex) in questionnaire.themes"
                   :theme="theme"
                   :theme-numbering="themeIndex + 1">

          <question-box v-for="(question, qIndex) in theme.questions"
                        :with-collapse="true"
                        :theme-numbering="themeIndex + 1"
                        :question-numbering="qIndex + 1"
                        :question="question">

            <question-file-list :question-id="question.id" :with-delete="false"></question-file-list>
            <response-file-list :question="question" :questionnaire-id="questionnaire.id" :is-audited="user.is_audited"></response-file-list>
            <response-dropzone :is-audited="user.is_audited"
                               :question-id="question.id">
            </response-dropzone>

          </question-box>

        </theme-box>
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
  import ThemeBox from '../themes/ThemeBox'
  import ThemeListSidebar from '../themes/ThemeListSidebar'

  const questionnaire_url = "/api/questionnaire/";
  const session_user_url = "/api/user/current/";

  export default Vue.extend({
    props: [ 'questionnaire'],
    data : function () {
      return {
        user: { is_audited: false },
      }
    },
    mounted: function(){
      this.getSessionUser()
    },
    methods: {
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
      ThemeBox,
      ThemeListSidebar,
    }
  })

</script>