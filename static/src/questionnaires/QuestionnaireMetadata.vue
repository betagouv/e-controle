<template>
  <div id="metadata" class="card">
    <div class="card-body">
      <p class="with-line-breaks">{{ questionnaire.description }}</p>
      <p v-if="questionnaire.sent_date">
        <i class="fe fe-send"></i>
        Date de transmission du questionnaire :
        {{ questionnaire.sent_date}}
      </p>

      <p v-if="questionnaire.end_date">
        <i class="fe fe-clock"></i>
        Date de réponse souhaitée :
        {{ questionnaire.end_date | DateFormat}}
      </p>

      <div class="text-right">
        <a :href="'/fichier-questionnaire/' + questionnaire.id" target="_blank">
          <button type="submit" class="btn btn-primary" title="Exporter ce questionnaire">
            <i class="fe fe-file-text mr-2"></i>
            Exporter ce questionnaire
          </button>
        </a>
      </div>
    </div>
  </div>
</template>

<script>
  import DateFormat from '../utils/DateFormat.js';
  import Vue from 'vue'

  export default Vue.extend({
    props: [ 'questionnaire' ],
    filters: {
      DateFormat
    },

  })

</script>
