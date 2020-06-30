<template>
  <div id="metadata" class="card">
    <div class="card-body">
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
        <div class="flex-row justify-content-end">
          <div v-if="withTrash" class="mx-2">
            <a class="btn btn-secondary"
              :href="trashUrl"
              title="Aller à la corbeille">
              <i class="fe fe-trash-2 mr-2"></i>Aller à la corbeille
            </a>
          </div>

          <button type="button"
                  class="btn btn-secondary dropdown-toggle dropdown-toggle-split mx-2"
                  data-toggle="dropdown"
                  aria-haspopup="true"
                  aria-expanded="false">
            <i class="fas fa-file-export mr-2"></i>
            <span class="mr-2">
              Exporter
            </span>
          </button>
          <div class="dropdown-menu dropdown-menu-right">
            <div class="dropdown-header">Questionnaire</div>
            <a class="dropdown-item"
              :href="exportUrl"
              target="_blank"
              rel="noopener noreferrer"
              title="Format Word (.docx)">
              <i class="fe fe-file-text mr-2"></i>Format Word (.docx)
            </a>
            <div v-if="!questionnaire.is_draft">
              <div class="dropdown-divider"></div>
              <div class="dropdown-header">Liste des réponses déposées</div>
              <a class="dropdown-item"
                :href="exportResponseFilesXlsxUrl"
                target="_blank"
                rel="noopener noreferrer"
                title="Format Excel (.xlsx)">
                <i class="far fa-file-excel mr-2"></i>
                Format Excel (.xlsx)
              </a>
            </div>
          </div>

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
    exportResponseFilesXlsxUrl() {
      return backendUrls['responses-export'](this.questionnaire.id)
    },
    trashUrl() {
      return backendUrls.trash(this.questionnaire.id)
    },
  },
})

</script>
