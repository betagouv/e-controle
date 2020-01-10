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
                       ref="swapEditorModal"
                       :control-id="controlId"
                       :questionnaire-id="questionnaireId"
                       @swap-editor="swapEditor"
                       @unset-editor="unsetEditor">
    </swap-editor-modal>
    <swap-editor-success-modal id="swapEditorSuccessModal"
                               :questionnaire-id="questionnaireId">
      <h4 class="mb-6">
        Les droits de rédaction ont été transférés à <br>
        {{ newEditor.first_name }} {{ newEditor.last_name }} !
      </h4>
      <p>
        Pour devenir rédacteur de ce questionnaire à nouveau, il faudra que
        votre collègue vous transfère ou libère les droits de rédaction.
      </p>
    </swap-editor-success-modal>
    <swap-editor-success-modal id="unsetEditorSuccessModal"
                               :questionnaire-id="questionnaireId">
      <h4 class="mb-6">
        Les droits de rédaction ont été libérés pour toute l'équipe !
      </h4>
      <p>
        Chaque membre de l'équipe peut maintenant prendre les droits pour devenir rédacteur.
      </p>
    </swap-editor-success-modal>

  </div>
</template>

<script>
import backendUrls from '../utils/backend.js'
import SwapEditorModal from '../editors/SwapEditorModal'
import SwapEditorSuccessModal from '../editors/SwapEditorSuccessModal'
import Vue from 'vue'

export default Vue.extend({
  props: [
    'controlId',
  ],
  data: function() {
    return {
      questionnaireId: undefined,
      newEditor: {},
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
    callSwapEditorApi(editorUser, questionnaireId) {
      const url = backendUrls.swapEditor(questionnaireId)
      return Vue.axios.put(url, {
        editor: editorUser,
      })
    },
    swapEditor(user) {
      this.callSwapEditorApi(user.id, this.questionnaireId)
        .then(result => {
          $('#swapEditorModal').modal('hide')
          this.newEditor = user
          $('#swapEditorSuccessModal').modal('show')
        })
        .catch(error => {
          this.$refs.swapEditorModal.showError('Le transfert de droits n\'a pas fonctionné. Vous pouvez réessayer. ' + error)
        })
    },
    unsetEditor() {
      this.callSwapEditorApi(null, this.questionnaireId)
        .then(result => {
          $('#swapEditorModal').modal('hide')
          $('#unsetEditorSuccessModal').modal('show')
        })
        .catch(error => {
          this.$refs.swapEditorModal.showError('Le transfert de droits n\'a pas fonctionné. Vous pouvez réessayer. ' + error)
        })
    },
  },
})
</script>
<style scoped>
</style>
