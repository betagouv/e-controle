<template>
  <div class="preview">
    <questionnaire-metadata :questionnaire="questionnaire">
    </questionnaire-metadata>

    <div>

      <theme-box v-for="(theme, themeIndex) in questionnaire.themes"
                 :theme="theme"
                 :theme-numbering="themeIndex + 1">

        <question-box v-for="(question, qIndex) in theme.questions"
                      :theme-numbering="themeIndex + 1"
                      :question-numbering="qIndex + 1"
                      :question="question">

          <question-file-list-without-vuex :question-id="question.id" :with-delete="false">
          </question-file-list-without-vuex>

        </question-box>

      </theme-box>

    </div>
  </div>
</template>

<script>
  import Vue from "vue";
  import QuestionBox from '../questions/QuestionBox.vue';
  import QuestionFileListWithoutVuex from "../questions/QuestionFileListWithoutVuex"
  import QuestionnaireMetadata from './QuestionnaireMetadata'
  import ThemeBox from '../themes/ThemeBox'

  export default Vue.extend({
    props: ['questionnaire'],
    data: function () {
      return {};
    },
    components: {
      QuestionBox,
      QuestionFileListWithoutVuex,
      QuestionnaireMetadata,
      ThemeBox,
    }
  });
</script>
