<template>
  <div class="mx-3">
    <breadcrumbs :control="control"></breadcrumbs>
    <template v-if="isLoaded && user.is_inspector">
      <request-editor-button
        :questionnaire="questionnaire"
        v-if="questionnaire.is_draft"
      >
      </request-editor-button>
      <success-bar v-else>
        Ce questionnaire est publié : il est visible par l'organisme contrôlé et
        n'est donc plus modifiable.
      </success-bar>
    </template>

    <div class="page-header">
      <div class="page-title">
        <i class="fe fe-list mr-2"></i>
        <template v-if="isLoaded && user.is_inspector">
          <span
            v-if="questionnaire.is_draft"
            class="tag tag-azure big-tag round-tag font-italic mr-2"
          >
            Brouillon
          </span>
          <span
            v-else-if="
              questionnaire_has_replies() && !questionnaire_is_replied()
            "
            class="tag tag-yellow round-tag font-italic mr-2"
            >En cours</span
          >
          <span
            v-else-if="
              questionnaire_is_replied() && !questionnaire_is_finalized()
            "
            class="tag tag-orange round-tag font-italic mr-2"
            >Répondu</span
          >
          <span
            v-else-if="questionnaire_is_finalized()"
            class="tag tag-purple round-tag font-italic mr-2"
            >Finalisé</span
          >
          <span v-else class="tag tag-green big-tag round-tag font-italic mr-2"
            >Publié</span
          >
        </template>
        {{ questionnaire.title_display }}
      </div>
    </div>
    <div :class="{ preview: questionnaire.is_draft }">
      <questionnaire-metadata
        :questionnaire="questionnaire"
        :with-trash="!questionnaire.is_draft"
      >
      </questionnaire-metadata>

      <div
        v-if="isLoaded && user.is_inspector && !questionnaire.is_draft"
        class="alert alert-info alert-icon"
      >
        <i class="fe fe-info" aria-hidden="true"></i>
        <div class="flex-row justify-content-end">
          <div>
            <p>
              Toutes les réponses déposées sont automatiquement classées et
              renomées dans un dossier dans votre Explorateur Windows. Découvrez
              comment les consulter !
            </p>
          </div>
          <div class="col-3 text-right pr-0">
            <button
              class="btn btn-primary parent-fake-icon"
              @click="showWebdavTip"
            >
              <i class="fe fe-folder mr-3"></i>
              <img
                :src="'/static/img/file-explorer.png'"
                alt="Explorateur Windows"
                class="fake-icon"
              />
              Voir les réponses
            </button>
          </div>
        </div>
      </div>
      <div>
        <theme-box
          v-for="(theme, themeIndex) in questionnaire.themes"
          :key="theme.id"
          :theme="theme"
          :theme-numbering="themeIndex + 1"
        >
          <question-box
            v-for="(question, qIndex) in theme.questions"
            :key="question.id"
            :with-collapse="true"
            :theme-numbering="themeIndex + 1"
            :question-numbering="qIndex + 1"
            :question="question"
          >
            <question-file-list :files="question.question_files">
            </question-file-list>
            <response-file-list
              :question="question"
              :questionnaire-id="questionnaire.id"
              :is-audited="isLoaded && user.is_audited"
            >
            </response-file-list>
            <response-dropzone
              :is-audited="isLoaded && user.is_audited"
              :is-replied="questionnaire.is_replied"
              :question-id="question.id"
            >
            </response-dropzone>
          </question-box>
        </theme-box>
      </div>
    </div>
    <webdav-tip
      v-if="!questionnaire.is_draft"
      ref="webdavTip"
      :control-id="questionnaire.control"
      :reference-code="control.reference_code"
    >
    </webdav-tip>
  </div>
</template>

<script>
import Vue from "vue";

import Breadcrumbs from "../utils/Breadcrumbs";
import { loadStatuses } from "../store";
import { mapState } from "vuex";
import QuestionBox from "../questions/QuestionBox";
import QuestionFileList from "../questions/QuestionFileList";
import QuestionnaireMetadata from "./QuestionnaireMetadata";
import RequestEditorButton from "../editors/RequestEditorButton";
import ResponseDropzone from "../questions/ResponseDropzone";
import ResponseFileList from "../questions/ResponseFileList";
import SuccessBar from "../utils/SuccessBar";
import ThemeBox from "../themes/ThemeBox";
import WebdavTip from "../controls/WebdavTip";

export default Vue.extend({
  name: "QuestionnaireDetailPage",
  props: {
    controlId: Number,
    questionnaireId: Number,
  },
  computed: {
    control() {
      return this.controls.find((control) => control.id === this.controlId);
    },
    questionnaire() {
      return this.control.questionnaires.find(
        (questionnaire) => questionnaire.id === this.questionnaireId
      );
    },
    ...mapState({
      // Note : we don't map controlsLoadStatus, because the only use of
      // this component is within a page which pre-fetches the data from server, so we know it is
      // already there.
      controls: "controls",
      user: "sessionUser",
      userLoadStatus: "sessionUserLoadStatus",
    }),
    isLoaded() {
      return this.userLoadStatus === loadStatuses.SUCCESS;
    },
  },
  methods: {
    questionnaire_is_replied() {
      return this.questionnaire.is_replied;
    },
    questionnaire_is_finalized() {
      return this.questionnaire.is_finalized;
    },
    questionnaire_has_replies() {
      const q = this.questionnaire;
      let found_replies = false;

      if (q.themes) {
        q.themes.map((theme) => {
          theme.questions.map((question) => {
            if (question.response_files.length) {
              found_replies = true;
            }
          });
        });
      }

      return found_replies;
    },
    showWebdavTip() {
      this.$refs.webdavTip.start();
    },
  },
  components: {
    Breadcrumbs,
    QuestionBox,
    QuestionFileList,
    QuestionnaireMetadata,
    RequestEditorButton,
    ResponseDropzone,
    ResponseFileList,
    SuccessBar,
    ThemeBox,
    WebdavTip,
  },
});
</script>
