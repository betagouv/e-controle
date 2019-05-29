<template>
  <div>
    <div v-if="questionnaire.metadata">
      <div v-if="questionnaire.metadata.title" class="card-header">
        <h3 class="card-title">{{questionnaire.metadata.title}}</h3>
      </div>
      <div id="metadata" class="card">
        <div class="card-body">
          <p>
            {{ questionnaire.metadata.description }}
          </p>
          <p v-if="questionnaire.metadata.sent_date">
            <i class="fe fe-send"></i>
            Date de transmission du questionnaire :
            {{ questionnaire.metadata.sent_date}}
          </p>

          <p v-if="questionnaire.metadata.end_date">
            <i class="fe fe-clock"></i>
            Date de réponse souhaitée :
            {{ questionnaire.metadata.end_date | DateFormat}}
          </p>
        </div>
      </div>
    </div>

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
                <tr v-for="(theme, themeIndex) in questionnaire.body" class="theme-row">
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
             v-for="(theme, themeIndex) in questionnaire.body"
             class="card">
          <div class="card-status card-status-top bg-blue"></div>
          <div class="card-header">
            <h3 class="card-title">{{ themeIndex + 1 }}. {{ theme.title }}</h3>
          </div>
          <div v-bind:id="'question' + (themeIndex + 1) + '.' + (qIndex + 1)"
               v-for="(question, qIndex) in theme.questions"
               class="card card-collapsed  border-0 m-0 p-0 pb-0 pt-2 {% cycle '' 'zebra' %}">
            <div class="card-header border-1" data-toggle="card-collapse">
              <span class="stamp stamp-md bg-blue mr-3" style="cursor: pointer">
                {{ themeIndex + 1 }}.{{ qIndex + 1 }}
              </span>
              <div class="card-text" style="cursor: pointer">
                {{ question.description }}
              </div>
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

  export default Vue.extend({
    props: ['questionnaire'],
    data: function () {
      return {};
    },
    filters: {
      DateFormat
    }
  });
</script>