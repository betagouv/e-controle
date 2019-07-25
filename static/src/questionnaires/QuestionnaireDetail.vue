<template>
  <div>
    <questionnaire-metadata :questionnaire="questionnaire">
    </questionnaire-metadata>

    <div id="body" class="row row-cards">
      <theme-list-sidebar :themes="questionnaire.themes">
      </theme-list-sidebar>

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
          </question-box>

        </div>
      </div>

    </div>
  </div>
</template>

<script>
  import Vue from "vue";
  import DateFormat from '../utils/DateFormat.js';
  import QuestionBox from '../questions/QuestionBox.vue';
  import QuestionFileList from "../questions/QuestionFileList"
  import QuestionnaireMetadata from './QuestionnaireMetadata'
  import ThemeListSidebar from '../themes/ThemeListSidebar'

  export default Vue.extend({
    props: ['questionnaire'],
    data: function () {
      return {};
    },
    filters: {
      DateFormat
    },
    components: {
      QuestionBox,
      QuestionFileList,
      QuestionnaireMetadata,
      ThemeListSidebar,
    }
  });
</script>
