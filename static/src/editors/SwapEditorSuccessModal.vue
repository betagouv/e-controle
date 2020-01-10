<template>
  <empty-modal no-close="true">
    <div class="modal-header pb-0 border-bottom-0 flex-column align-items-center">
      <i class="fe fe-check-circle fg-success big-icon"></i>
    </div>
    <div class="modal-body text-center">
      <h4 class="mb-6">
        Les droits de rédaction ont été transférés !
      </h4>
      <p>
        Pour devenir rédacteur de ce questionnaire à nouveau, il faudra que
        votre collègue transfère ou libère les droits de rédaction.
      </p>
    </div>
    <div class="modal-footer border-top-0 d-flex justify-content-center">
      <button @click="goToReadonlyPage()" role="button" class="btn btn-primary px-7">
        OK
      </button>
    </div>
  </empty-modal>
</template>

<script>
import Vue from 'vue'
import EmptyModal from '../utils/EmptyModal'
import backendUrls from '../utils/backend.js'

export default Vue.extend({
  props: ['questionnaireId'],
  methods: {
    goToReadonlyPage() {
      const url = backendUrls['questionnaire-detail'](this.questionnaireId)
      window.location.assign(url)
    },
  },
  components: {
    EmptyModal,
  },
})
</script>
