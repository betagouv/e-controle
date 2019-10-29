<template>
  <div>
    <div class="page-header">
      <div class="page-title">
        <i class="fe fe-list mr-2"></i>
        <span v-if="questionnaire.is_draft" class="tag tag-azure big-tag round-tag font-italic mr-2">Brouillon</span>{{ questionnaire.title_display }}
      </div>
    </div>
    <info-bar v-if="questionnaire.is_draft">
      <span v-if="questionnaire.author">{{ questionnaire.author.first_name }} {{ questionnaire.author.last_name }}</span>
      <span v-else>[INCONNU]</span>
      a créé ce brouillon. Il/elle en est rédacteur et est le/la seule à pouvoir le modifier. Suggérez-lui vos modifications.
    </info-bar>
    <div :class="{ preview: questionnaire.is_draft }">
      <questionnaire-metadata :questionnaire="questionnaire" :with-trash="!questionnaire.is_draft">
      </questionnaire-metadata>

      <div>
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
  import InfoBar from '../utils/InfoBar'
  import QuestionBox from '../questions/QuestionBox'
  import QuestionFileList from '../questions/QuestionFileList'
  import QuestionnaireMetadata from './QuestionnaireMetadata'
  import ResponseDropzone from '../questions/ResponseDropzone'
  import ResponseFileList from '../questions/ResponseFileList'
  import ThemeBox from '../themes/ThemeBox'

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
      InfoBar,
      QuestionBox,
      QuestionFileList,
      QuestionnaireMetadata,
      ResponseDropzone,
      ResponseFileList,
      ThemeBox,
    }
  })

</script>