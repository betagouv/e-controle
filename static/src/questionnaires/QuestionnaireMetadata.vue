<template>
  <div id="metadata" class="card">
    <div class="card-body flex-row justify-content-between align-items-center">
      <div>
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
      </div>

      <div class="flex-column text-right">
        <div class="card-footer border-0">
          <a class="btn btn-primary"
             :href="exportUrl"
             target="_blank"
             title="Exporter ce questionnaire">
            <i class="fe fe-file-text mr-2"></i>Exporter ce questionnaire
          </a>
        </div>
        <div v-if="withTrash" class="card-footer border-0">
          <a class="btn btn-primary"
             :href="'/questionnaire/corbeille/' + questionnaire.id"
             title="Aller à la corbeille">
            <i class="fe fe-trash-2 mr-2"></i>Aller à la corbeille
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import backendUrls from '../utils/backend'
import DateFormat from '../utils/DateFormat.js'
import Vue from 'vue'

export default Vue.extend({
  props: ['questionnaire', 'withTrash'],
  filters: {
    DateFormat,
  },
  computed: {
    exportUrl() {
      return backendUrls['questionnaire-export'](this.questionnaire.id)
    },
  },
})

</script>
