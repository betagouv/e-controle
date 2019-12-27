<template>
  <div class="modal" tabindex="-1" role="dialog">
    <div class="modal-dialog large-modal" role="document">
      <div class="modal-content">
        <div class="modal-header border-bottom-0">
          <i class="fa fa-exchange-alt mr-2 mt-3"></i>
          <div class="modal-title">
            <h3 class="modal-title">Obtenir les droits de rédaction du questionnaire</h3>
          </div>
          <button type="button"
                  class="close"
                  data-dismiss="modal"
                  aria-label="Close">
          </button>
        </div>

        <div class="modal-body">
          <div class="row row-cards row-deck">
            <div class="col">
              <div class="card">
                <div class="card-body">
                  <h4 class="mb-0">Contactez votre collègue {{ questionnaire.editor.first_name }} {{ questionnaire.editor.last_name }}</h4>
                  (<a :href="'mailto:' + questionnaire.editor.email">{{ questionnaire.editor.email }}</a>)
                  <p class="mt-4">Pour modifier ce questionnaire, votre collègue doit vous transférer les droits.</p>
                </div>
                <img :src="'/static/img/call-for-help.png'" alt="appel à l'aide">
              </div>
            </div>
            <div class="col">
              <div class="card">
                <div class="card-body">
                  <h4>Votre collègue n'est pas disponible ?</h4>
                  <p>Vous pouvez forcer le transfert des droits.</p>
                  <div class="alert alert-icon alert-danger" role="alert">
                    <i class="fe fe-alert-triangle mr-2" aria-hidden="true"></i>
                    Attention, dans ce cas toute modification non enregistrée par votre collègue sera perdue.
                  </div>
                  <div class="mb-4" v-if="questionnaire.modified_date">
                    Dernier enregistrement de ce questionnaire :
                    <br />{{ questionnaire.modified_date }} à
                    {{  questionnaire.modified_time }}
                  </div>
                  <button type="submit"
                    class="btn btn-secondary"
                    title="Forcer le transfert des droits"
                    data-toggle="modal"
                    data-target="#becomeEditorModal"
                    @click="clickBecomeEditor()">
                    <i class="fa fa-exchange-alt mr-1"></i>
                    Forcer le transfert des droits
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div class="card">
            <div class="card-body alert alert-info" role="alert">
              <div class="mb-4">
                <h4><i class="fe fe-help-circle mr-1"></i>Un problème, une question ?</h4>
                Nous sommes là pour vous aider. N'hésitez pas à prendre contact avec l'équipe e.contrôle !
              </div>
              <a role="button"
                  type="submit"
                  :href="'mailto:' + config.support_team_email"
                  class="btn btn-primary"
                  title="Contacter le support e.contrôle">
                <i class="fe fe-mail mr-1"></i>
                Contacter le support e.contrôle
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapFields } from 'vuex-map-fields'
import backendUrls from '../utils/backend.js'
import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default Vue.extend({
  props: ['questionnaire'],
  computed: {
    ...mapFields(['config']),
  },
  methods: {
    callSwapEditorApi(editorUser, questionnaireId) {
      const url = '/api' + backendUrls['swap-editor'](questionnaireId)
      Vue.axios.put(url, {
        editor: editorUser,
      }).then((response) => {
        this.postResult = response.data
      })
    },
    SetEditorNull() {
      this.callSwapEditorApi(null, this.questionnaire.id)
      $('#swapEditorModal').modal('hide')
    },
    clickBecomeEditor() {
      $('#requestEditorModal').modal('hide')
    },
  },
});
</script>
<style scoped>
.large-modal {
    width: 1000px;
    max-width: 100%;
    margin: 2% auto;
}
</style>
