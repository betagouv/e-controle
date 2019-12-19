<template>
    <div class="modal" tabindex="-1" role="dialog">
      <div class="modal-dialog large-modal" role="document">
        <div class="modal-content">
          <div class="modal-header border-bottom-0">
            <i class="fa fa-exchange-alt mr-2 mt-3"></i>
            <div class="modal-title">
            <h3 class="modal-title">Transférer les droits de rédaction du questionnaire</h3>
            </div>
            <button type="button"
                    class="close"
                    data-dismiss="modal"
                    aria-label="Close">
            </button>
          </div>

          <div class="modal-body">
            <p class="ml-6">
              Vous pouvez permettre à vos collègues de modiffier à leur tour le questionnaire.
              <br/>Pour pouvoir le modifier, un de vos collègues devra à son tour vous transférer les droits.
              </p>

            <div class="card-body">
              <div class="card">
                <div class="card-header justify-content-between">
                  <h3 class="card-title"><i class="fa fa-university mr-2"></i><strong>Équipe de contrôle</strong></h3>
                </div>

                <editor-list :users="inspectorUsers()" :questionnaireId='questionnaireId'></editor-list>
              </div>

              <div class="card">
                <div class="card-body">
                  <div class="flex-row align-items-center">
                    <div class="flex-column mr-4 flex-grow-1">
                      <strong>Libérer les droits de rédaction pour toutes l'équipe</strong>
                      <p>Chacun.e de vos collègues pourra à son tour les prendre pour rédiger.</p>
                    </div>
                    <div class="flex-column mr-4">
                      <button
                        class="btn btn-primary"
                        title="Transférer"
                        data-toggle="modal"
                        data-target="#swapEditorSuccessModal"
                        @click="SetEditorNull()">
                          <i class="fa fa-lock-open mr-2"></i>
                          Libérer les droits
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
                    <button type="submit"
                      class="btn btn-primary"
                      title="Contacter le support e-contrôle">
                      <i class="fe fe-mail mr-1"></i>
                      Contacter le support e.contrôle
                    </button>
                  </div>
              </div>

          </div>
        </div>
      </div>
    </div>
</template>

<script>
import axios from 'axios'
import backendUrls from '../utils/backend.js'
import EditorList from './EditorList'
import Vue from 'vue'
import VueAxios from 'vue-axios'

Vue.use(VueAxios, axios)

export default Vue.extend({
  props: [
    'controlId',
    'questionnaireId',
  ],
  data() {
    return {
      users: [],
    }
  },
  methods: {
    getUsers() {
      Vue.axios.get(backendUrls.user(), {
        params: {
          controls: this.controlId,
        },
      }).then((response) => {
        this.users = response.data
      })
    },
    inspectorUsers() {
      return this.users.filter(item => {
        return item.profile_type === 'inspector'
      })
    },
    callSwapEditorApi(editorUser, questionnaireId) {
      const url = '/api' + backendUrls['swap-editor'](questionnaireId)
      Vue.axios.put(url, {
        editor: editorUser,
      }).then((response) => {
        this.postResult = response.data
      })
    },
    SetEditorNull() {
      this.callSwapEditorApi(null, this.questionnaireId)
      $('#swapEditorModal').modal('hide')
    },
  },
  components: {
    EditorList,
  },
  mounted() {
    this.getUsers()
},
})
</script>
<style scoped>
  .large-modal {
      width: 1000px;
      max-width: 100%;
      margin: 2% auto;
  }
</style>
