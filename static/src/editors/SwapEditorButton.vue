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
          data-toggle="modal"
          data-target="#swapEditorModal">
          <i class="fa fa-exchange-alt mr-1"></i>
          Transférer les droits de rédaction...
        </button>
        </div>
    </div>

    <swap-editor-modal id="swapEditorModal"
                       :control-id='controlId'
                       :questionnaire-id='questionnaireId'>
    </swap-editor-modal>
    <swap-editor-success-modal id="swapEditorSuccessModal"></swap-editor-success-modal>
  </div>
</template>

<script>
import Vue from 'vue'
import SwapEditorModal from '../editors/SwapEditorModal'
import SwapEditorSuccessModal from '../editors/SwapEditorSuccessModal'

export default Vue.extend({
  props: [
    'controlId',
    'questionnaireId',
  ],
  components: {
    SwapEditorModal,
    SwapEditorSuccessModal,
  },
})
</script>
<style scoped>
</style>
