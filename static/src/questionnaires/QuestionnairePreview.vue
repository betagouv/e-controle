<template>
  <div>
    <div class="card">
      <div class="card-header">
        <div class="card-title">Etape 3 : Aperçu avant publication</div>
      </div>
      <div class="card-body pb-6">
        <questionnaire-detail-for-preview v-bind:questionnaire="currentQuestionnaire">
        </questionnaire-detail-for-preview>
      </div>
    </div>

  </div>
</template>

<script>
import Vue from 'vue'
import { mapFields } from 'vuex-map-fields'
import QuestionnaireDetailForPreview from './QuestionnaireDetailForPreview'

export default Vue.extend({
  computed: {
    ...mapFields([
      'currentQuestionnaire',
    ]),
  },
  components: {
    QuestionnaireDetailForPreview,
  },
})
</script>

<style>
</style>
