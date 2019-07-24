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

      <div class="col-lg-8" id="question-detail-app">
        <div v-bind:id="'theme' + (themeIndex + 1)"
             v-for="(theme, themeIndex) in questionnaire.themes"
             class="card">
          <div class="card-status card-status-top bg-blue"></div>
          <div class="card-header">
            <h3 class="card-title">{{ themeIndex + 1 }}. {{ theme.title }}</h3>
          </div>
          <div v-bind:id="'question' + (themeIndex + 1) + '.' + (qIndex + 1)"
               v-for="(question, qIndex) in theme.questions"
               class="card m-0 p-0 pb-0">
            <div class="card-header border-0" data-toggle="card-collapse">
              <question :question_description="question.description"
                        :theme_numbering="themeIndex + 1"
                        :question_numbering="qIndex + 1"
                        :question_id="question.id"
                        :annexe_count="question.question_files && question.question_files.length">
              </question>
            </div>
            <div class="card-body">
              <question-file-list :question-id="question.id" :with-delete="false"></question-file-list>
            </div>

          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import Vue from "vue";
  import DateFormat from '../utils/DateFormat.js';
  import Question from '../details/Question.vue';
  import QuestionFileList from "./QuestionFileList"
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
      Question,
      QuestionFileList,
      QuestionnaireMetadata,
    }
  });
</script>
