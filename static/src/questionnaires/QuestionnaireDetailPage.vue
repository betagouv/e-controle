<template>
  <div class="container">
    <template v-if="user.is_inspector">
      <request-editor-button :questionnaire='questionnaire'  v-if="questionnaire.is_draft"></request-editor-button>
      <success-bar v-else>
        Ce questionnaire est publié : il est visible par l'organisme contrôlé et n'est donc plus modifiable.
      </success-bar>
    </template>

    <div class="page-header">
      <div class="page-title">
        <i class="fe fe-list mr-2"></i>
        <template v-if="user.is_inspector">
          <span v-if="questionnaire.is_draft" class="tag tag-azure big-tag round-tag font-italic mr-2">Brouillon</span>
          <span v-else class="tag tag-green big-tag round-tag font-italic mr-2">Publié</span>
        </template>
        {{ questionnaire.title_display }}
      </div>
    </div>
    <div :class="{ preview: questionnaire.is_draft }">
      <questionnaire-metadata :questionnaire="questionnaire" :with-trash="!questionnaire.is_draft">
      </questionnaire-metadata>

      <div v-if="user.is_inspector" class="alert alert-info alert-icon">
        <i class="fe fe-info" aria-hidden="true"></i>
        <div class="flex-row justify-content-end">
          <div>
            <p>
              Toutes les réponses déposées sont automatiquement classées et renomées dans un dossier
              dans votre Explorateur Windows. Découvrez comment les consulter !
            </p>
          </div>
          <div class="col-3 text-right pr-0">
            <button class="btn btn-primary btn-fake-icon" @click="showWebdavTip">
              <img :src="'/static/img/file-explorer.png'"
                  alt="Explorateur Windows"
                  class="fake-icon mr-2" />
              Voir les réponses
            </button>
          </div>
        </div>
      </div>
      <div>
        <theme-box v-for="(theme, themeIndex) in questionnaire.themes"
                   :theme="theme"
                   :theme-numbering="themeIndex + 1">

          <question-box v-for="(question, qIndex) in theme.questions"
                        :with-collapse="true"
                        :theme-numbering="themeIndex + 1"
                        :question-numbering="qIndex + 1"
                        :question="question">

            <question-file-list-without-vuex :question-id="question.id">
            </question-file-list-without-vuex>
            <response-file-list :question="question" :questionnaire-id="questionnaire.id" :is-audited="user.is_audited"></response-file-list>
            <response-dropzone :is-audited="user.is_audited"
                               :question-id="question.id">
            </response-dropzone>

          </question-box>

        </theme-box>

      </div>
    </div>
    <webdav-tip :id="'webdav-tip-' + questionnaire.control"
                :reference-code="questionnaire.control_reference_code">
    </webdav-tip>
  </div>

</template>

<script>
  import Vue from "vue";

  import axios from 'axios'
  import QuestionBox from '../questions/QuestionBox'
  import QuestionFileListWithoutVuex from '../questions/QuestionFileListWithoutVuex'
  import QuestionnaireMetadata from './QuestionnaireMetadata'
  import RequestEditorButton from '../editors/RequestEditorButton'
  import ResponseDropzone from '../questions/ResponseDropzone'
  import ResponseFileList from '../questions/ResponseFileList'
  import SuccessBar from '../utils/SuccessBar'
  import ThemeBox from '../themes/ThemeBox'
  import WebdavTip from '../controls/WebdavTip'

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
      showWebdavTip() {
        $('#webdav-tip-' + this.questionnaire.control).modal('show')
      },
    },
    components: {
      QuestionBox,
      QuestionFileListWithoutVuex,
      QuestionnaireMetadata,
      RequestEditorButton,
      ResponseDropzone,
      ResponseFileList,
      SuccessBar,
      ThemeBox,
      WebdavTip,
    }
  })

</script>
