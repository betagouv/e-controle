<template>
  <div>
    <empty-modal ref="confirmModal" class="confirm-modal" :no-close="true">
      <form @submit.prevent="deleteControl">
        <div class="modal-header border-bottom-0">
          <h4 class="modal-title">
            <div class="mb-4">
              Vous êtes sur le point de supprimer :
            </div>
            <div>
              Questionnaire {{ questionnaire.numbering }} : {{ questionnaire.title }}
            </div>
          </h4>
        </div>

        <div class="modal-body">
          <label class="custom-control custom-checkbox">
            <input type="checkbox"
                   class="custom-control-input"
                   required>
            <span class="custom-control-label">Les données ne seront pas récupérables.</span>
          </label>
          <label class="custom-control custom-checkbox">
            <input type="checkbox"
                   class="custom-control-input"
                   required>
            <span class="custom-control-label">
              Tous les utilisateurs de cet espace n'y auront plus accès.
            </span>
          </label>
          <label class="custom-control custom-checkbox">
            <input type="checkbox"
                   class="custom-control-input"
                   required>
            <span class="custom-control-label">
              En cas de contrôle juridictionnel, je confirme que la suppression
              des données, n'impacte pas la suite de la procédure, en cas de
              contentieux notament.
            </span>
          </label>
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
    </empty-modal>
    <empty-modal ref="waitingModal"
                 no-close="true">
      <div class="d-flex flex-column align-items-center p-8">
        <div class="m-4">
          Suppression en cours...
        </div>
        <div class="loader m-4"></div>
      </div>
    </empty-modal>
    <empty-modal ref="successModal"
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
      $(this.$refs.confirmModal.$el).modal('hide')
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
