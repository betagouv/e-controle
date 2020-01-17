<template>
  <div>
    <div class="alert alert-secondary" role="alert">
      <div class="flex-row justify-content-between align-items-center">
        <div>
          <i class="fe fe-users mr-1"></i>
          <span v-if="questionnaire.editor">
            <strong>{{ questionnaire.editor.first_name }} {{ questionnaire.editor.last_name }}</strong>
            est actuellement la seule personne qui peut modifier ce questionnaire.
          </span>
          <span v-else>
            Personne n'est actuellement affecté à la rédaction de ce questionnaire.
          </span>
        </div>
        <div class="text-right">
          <button v-if="questionnaire.editor"
            type="submit"
            class="btn btn-gray obtain-rights-button"
            title="Obtenir les droits de rédaction..."
            data-toggle="modal"
            data-target="#requestEditorModal">
            <i class="fa fa-exchange-alt mr-1"></i>
            <span>Obtenir les droits de rédaction...</span>
          </button>
          <button v-else
            type="submit"
            class="btn btn-gray obtain-rights-button"
            title="Obtenir les droits de rédaction..."
            @click="takeEditorRights"
            >
            <i class="fa fa-exchange-alt mr-1"></i>
            <span>Obtenir les droits de rédaction...</span>
          </button>
        </div>
      </div>
      <error-bar v-if="errorMessage.length > 0" class="mt-4">
        {{ errorMessage }}
      </error-bar>
    </div>

    <request-editor-modal id="requestEditorModal"
                          :questionnaire="questionnaire"
                          @request-editor="requestEditor">
    </request-editor-modal>

    <request-editor-confirm-modal id="requestEditorConfirmModal"
                                  @confirm="takeEditorRights">
    </request-editor-confirm-modal>

  </div>
</template>

<script>
import axios from 'axios'
import backendUrls from '../utils/backend.js'
import RequestEditorConfirmModal from '../editors/RequestEditorConfirmModal'
import ErrorBar from '../utils/ErrorBar'
import { mapFields } from 'vuex-map-fields'
import RequestEditorModal from '../editors/RequestEditorModal'
import Vue from 'vue'

export default Vue.extend({
  props: {
    questionnaire: {},
    // Pass window object as prop, so that we can pass a mock for testing.
    // Do not use "window" or "document" directly in this file, instead use "this.window" and
    // "this.window.document"
    window: {
      default: () => window,
    },
  },
  data: function() {
    return {
      errorMessage: '',
    }
  },
  components: {
    ErrorBar,
    RequestEditorConfirmModal,
    RequestEditorModal,
  },
  computed: {
    ...mapFields(['sessionUser']),
  },
  methods: {
    callSwapEditorApi(editorUser, questionnaireId) {
      const url = backendUrls.swapEditor(questionnaireId)
      return axios.put(url, {
        editor: editorUser,
      })
    },
    takeEditorRights: function() {
      this.errorMessage = ''
      this.callSwapEditorApi(this.sessionUser.id, this.questionnaire.id)
        .then((response) => {
          console.debug('got editing rights', response)
          this.window.location.assign(backendUrls['questionnaire-edit'](this.questionnaire.id))
        })
        .catch(error => {
          console.error(error)
          this.errorMessage = 'Erreur lors de l\'obtention des droits. Vous pouvez réessayer.'
        })
    },
    requestEditor: function() {
      $('#requestEditorModal').modal('hide')
      $('#requestEditorConfirmModal').modal('show')
    },
  },
})
</script>
<style scoped>
</style>
