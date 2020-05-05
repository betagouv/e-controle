<template>
  <div class="page-main flex-row">
    <div id="sidebar-vm" class="border-right">
      <sidebar></sidebar>
    </div>
    <div class="mt-3 mt-md-5 flex-grow-1 ml-6 ie-flex-row-child">
      <questionnaire-detail-page :control="control" :questionnaire-id="questionnaireId">
      </questionnaire-detail-page>
    </div>
  </div>
</template>

<script>
import QuestionnaireDetailPage from './QuestionnaireDetailPage'
import Sidebar from '../utils/Sidebar'
import Vue from 'vue'

export default Vue.extend({
  name: 'QuestionnaireDetail',
  props: {
    control: Object,
    questionnaireId: Number,
  },
  components: {
    QuestionnaireDetailPage,
    Sidebar,
  },
})
</script>
