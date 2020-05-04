<template>
  <div class="preview">
    <questionnaire-metadata :questionnaire="questionnaire">
    </questionnaire-metadata>

    <div>

      <theme-box v-for="(theme, themeIndex) in questionnaire.themes"
                 :key="theme.id"
                 :theme="theme"
                 :theme-numbering="themeIndex + 1">

        <question-box v-for="(question, qIndex) in theme.questions"
                      :key="question.id"
                      :theme-numbering="themeIndex + 1"
                      :question-numbering="qIndex + 1"
                      :question="question">

          <question-file-list :files="question.question_files">
          </question-file-list>

        </question-box>

      </theme-box>

    </div>
  </div>
</template>

<script>
import Vue from 'vue'
import QuestionBox from '../questions/QuestionBox.vue'
import QuestionFileList from '../questions/QuestionFileList'
import QuestionnaireMetadata from './QuestionnaireMetadata'
import ThemeBox from '../themes/ThemeBox'

export default Vue.extend({
  props: ['questionnaire'],
  data: function () {
    return {}
  },
  components: {
    QuestionBox,
    QuestionFileList,
    QuestionnaireMetadata,
    ThemeBox,
  },
})
</script>
