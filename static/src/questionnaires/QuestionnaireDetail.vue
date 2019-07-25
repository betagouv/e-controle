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
                        :theme-index="themeIndex"
                        :question-index="qIndex"
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
    }
  });
</script>
