<template>
  <div>
    <empty-modal id="questionnaireDeleteModal"
                ref="questionnaireDeleteModal"
                :no-close="true">
      <div class="modal-body">
        <form @submit.prevent="deleteControl">
          <div class="modal-header border-bottom-0">
            <h4 class="modal-title">
              Vous êtes sur le point de supprimer le questionnaire :
            </h4>
          </div>

          <div class="modal-body">
            <div class="flex-row">
              <input class="mt-2"
                    type="checkbox"
                    name="questionnaire-delete-checkbox-1"
                    id="questionnaire-delete-checkbox-1"
                    required>
              <label class="ml-2" for="questionnaire-delete-checkbox-1">
                Les données ne seront pas récupérables.
              </label>
            </div>
            <div class="flex-row">
              <input class="mt-2"
                    type="checkbox"
                    name="questionnaire-delete-checkbox-2"
                    id="questionnaire-delete-checkbox-2"
                    required>
              <label class="ml-2" for="questionnaire-delete-checkbox-2">
                Tous les utilisateurs de cet espace n'y auront plus accès.
              </label>
            </div>
            <div class="flex-row">
              <input class="mt-2"
                    type="checkbox"
                    name="questionnaire-delete-checkbox-3"
                    id="questionnaire-delete-checkbox-3"
                    required>
              <label class="ml-2" for="questionnaire-delete-checkbox-3">
                En cas de contrôle juridictionnel, je confirme que la suppression
                des données, n'impacte pas la suite de la procédure, en cas de
                contentieux notament.
              </label>
            </div>
          </div>
          <div class="modal-footer border-top-0">
            <button type="button"
                    class="btn btn-secondary"
                    data-dismiss="modal"
                    title="Annuler"
            >
              Annuler
            </button>
            <button type="submit"
                    class="btn btn-primary btn-red"
                    title="Forcer le transfert"
            >
              <i class="fe fe-trash-2 mr-1"></i>
              Supprimer
            </button>
          </div>
        </form>
      </div>
    </empty-modal>
    <empty-modal id="waitingModal"
                 ref="waitingModal"
                 no-close="true">
      <div class="d-flex flex-column align-items-center p-8">
        <div class="m-4">
          Suppression en cours...
        </div>
        <div class="loader m-4"></div>
      </div>
    </empty-modal>
    <empty-modal id="successModal"
                 ref="successModal"
                 no-close="true">
      <div class="modal-header border-bottom-0 flex-column align-items-center">
        <p>
          <i class="fe fe-check-circle fg-success big-icon"></i>
        </p>
        <p class="text-center">
          Le questionnaire à bien été supprimé.
        </p>
      </div>
      <div class="modal-footer border-top-0 d-flex justify-content-center">
        <button type="button"
                class="btn btn-primary"
                @click="done"
        >
          Terminer
        </button>
      </div>
    </empty-modal>
  </div>
</template>

<script>
import backendUrls from '../utils/backend.js'
import EmptyModal from '../utils/EmptyModal'
import Vue from 'vue'

const SPINNER_DURATION_MILLIS = 2000


export default Vue.extend({
  props: {
    questionnaire: Object,
  },
  components: {
    EmptyModal,
  },
  methods: {
    wait(timeMillis) {
      return new Promise((resolve) => {
        const id = setTimeout(() => {
          clearTimeout(id)
          resolve()
        }, timeMillis)
      })
    },
    done() {
      $(this.$refs.successModal.$el).modal('hide')
    },
    callDeleteControlAPI() {
      console.log('calling API...')
    },
    deleteControl() {
      $(this.$refs.questionnaireDeleteModal.$el).modal('hide')
      $(this.$refs.waitingModal.$el).modal('show')

      return Promise.all([this.wait(SPINNER_DURATION_MILLIS), this.callDeleteControlAPI()])
        .then(() => {
          console.debug('Done deleting questionnaire.')
          $(this.$refs.waitingModal.$el).modal('hide')
          $(this.$refs.successModal.$el).modal('show')
        })
        .catch(error => {
          console.error('Error deleting questionnaire : ', error)
        })
    },
  },
})
</script>

<style scoped>

</style>
