<template>
  <div>
    <div class="alert alert-info flex-row justify-content-between" role="alert">
        <div class="mt-2">
        <i class="fe fe-users mr-1"></i>
        <strong>Vous</strong> êtes actuellement le rédacteur de ce questionnaire.
        </div>
        <div class="text-right">
        <button type="submit"
          class="btn btn-primary"
          title="Transférer les droits de rédaction..."
          @click="saveDraft">
          <i class="fa fa-exchange-alt mr-1"></i>
          Transférer les droits de rédaction...
        </button>
        </div>
    </div>

    <swap-editor-modal id="swapEditorModal"
                       :control-id="controlId"
                       :questionnaire-id="questionnaireId">
    </swap-editor-modal>
    <swap-editor-success-modal id="swapEditorSuccessModal"
                               :questionnaire-id="questionnaireId">
      <h4 class="mb-6">
        Les droits de rédaction ont été transférés !
      </h4>
      <p>
        Pour devenir rédacteur de ce questionnaire à nouveau, il faudra que
        votre collègue transfère ou libère les droits de rédaction.
      </p>
    </swap-editor-success-modal>
    <swap-editor-success-modal id="unsetEditorSuccessModal"
                               :questionnaire-id="questionnaireId">
      <h4 class="mb-6">
        Les droits de rédaction ont été libérés pour toute l'équipe !
      </h4>
      <p>
        Pour devenir rédacteur de ce questionnaire à nouveau, il faudra que
        votre collègue transfère ou libère les droits de rédaction.
      </p>
    </swap-editor-success-modal>

  </div>
</template>

<script>
import Vue from 'vue'
import SwapEditorModal from '../editors/SwapEditorModal'
import SwapEditorSuccessModal from '../editors/SwapEditorSuccessModal'

export default Vue.extend({
  props: [
    'controlId',
  ],
  data: function() {
    return {
      questionnaireId: undefined,
    }
  },
  components: {
    SwapEditorModal,
    SwapEditorSuccessModal,
  },
  mounted: function() {
    const showModal = (questionnaireId) => {
      console.debug('got questionnaire id', questionnaireId)
      this.questionnaireId = questionnaireId
      $('#swapEditorModal').modal('show')
    }

    this.$parent.$on('show-swap-editor-modal', showModal.bind(this))
  },
  methods: {
    saveDraft: function() {
      this.$emit('save-draft')
    },
  },
})
</script>
<style scoped>
</style>
