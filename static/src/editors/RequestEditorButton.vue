<template>
  <div>
    <div class="alert alert-secondary" role="alert">
      <div class="flex-row justify-content-between align-items-center">
        <div>
          <i class="fe fe-users mr-1"></i>
          <span v-if="questionnaire.editor">
            <strong>{{ questionnaire.editor.first_name }} {{ questionnaire.editor.last_name }}</strong>
            est actuellement la seule personne qui peut modifier ce questionnaire
          </span>
          <span v-else>
            Personne n'est actuellement affecté à la rédaction de ce questionnaire.
          </span>
        </div>
        <div class="text-right">
          <button v-if="questionnaire.editor"
            type="submit"
            class="btn btn-gray"
            title="Obtenir les droits de rédaction..."
            data-toggle="modal"
            data-target="#requestEditorModal">
            <i class="fa fa-exchange-alt mr-1"></i>
            <span>Obtenir les droits de rédaction...</span>
          </button>
          <button v-else
            type="submit"
            class="btn btn-gray"
            title="Obtenir les droits de rédaction..."
            @click="switchToEditorPage"
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
    <request-editor-modal id="requestEditorModal" :questionnaire='questionnaire'></request-editor-modal>
    <become-editor-modal id="becomeEditorModal" :questionnaire-id='questionnaire.id'></become-editor-modal>
  </div>
</template>

<script>
import backendUrls from '../utils/backend.js'
import BecomeEditorModal from '../editors/BecomeEditorModal'
import ErrorBar from '../utils/ErrorBar'
import { mapFields } from 'vuex-map-fields'
import RequestEditorModal from '../editors/RequestEditorModal'
import Vue from 'vue'

export default Vue.extend({
  props: ['questionnaire'],
  data: function() {
    return {
      errorMessage: '',
    }
  },
  components: {
    BecomeEditorModal,
    ErrorBar,
    RequestEditorModal,
  },
  computed: {
    ...mapFields(['sessionUser']),
  },
  methods: {
    callSwapEditorApi(editorUser, questionnaireId) {
      const url = '/api' + backendUrls['swap-editor'](questionnaireId)
      return Vue.axios.put(url, {
        editor: editorUser,
      })
    },
    switchToEditorPage: function() {
      this.errorMessage = ''
      this.callSwapEditorApi(this.sessionUser.id, this.questionnaire.id)
        .then((response) => {
          console.debug('got editing rights', response)
          window.location.assign(backendUrls['questionnaire-edit'](this.questionnaire.id))
        })
        .catch(error => {
          console.error(error)
          this.errorMessage = 'Erreur lors de l\'obtention des droits. Vous pouvez réessayer.'
        })
    },
  },
})
</script>
<style scoped>
</style>
