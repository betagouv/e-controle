<template>
  <div>
      <div class="alert alert-secondary flex-row justify-content-between" role="alert">
        <div class="mt-2">
        <i class="fe fe-users mr-1"></i>
        <span v-if="questionnaire.editor"><strong>{{ questionnaire.editor.first_name }} {{ questionnaire.editor.last_name }}</strong></span>
        <span v-else>[INCONNU]</span>
        est actuellement la seule personne qui peut modifier ce questionnaire
        </div>
        <div class="text-right">
        <button type="submit"
          class="btn btn-gray"
          title="Demander les droits de rédaction..."
          data-toggle="modal"
          data-target="#requestEditorModal">
          <i class="fa fa-exchange-alt mr-1"></i>
          Demander les droits de rédaction...
        </button>
        </div>
    </div>
    <request-editor-modal id="requestEditorModal" :questionnaire='questionnaire'></request-editor-modal>
    <become-editor-modal id="becomeEditorModal" :questionnaire-id='questionnaire.id'></become-editor-modal>
  </div>
</template>

<script>
import Vue from 'vue'
import BecomeEditorModal from '../editors/BecomeEditorModal'
import RequestEditorModal from '../editors/RequestEditorModal'

export default Vue.extend({
  props: ['questionnaire'],
  components: {
    RequestEditorModal,
    BecomeEditorModal,
  },
})
</script>
<style scoped>
</style>
