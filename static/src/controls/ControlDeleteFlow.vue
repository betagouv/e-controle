<template>
  <modal-flow ref="modalFlow" :action-function="callDeleteControlAPI">

    <template v-slot:confirm-modal-form>
      <div class="modal-header border-bottom-0">
        <h4 class="modal-title">
          <div class="mb-4">
            Vous êtes sur le point de supprimer l'espace de dépôt :
          </div>
          <div>
            "{{ control.title }}"
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
            contentieux notamment.
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
                title="Supprimer l'espace de dépôt"
        >
          <i class="fe fe-trash-2 mr-1"></i>
          Supprimer
        </button>
      </div>
    </template>

    <template v-slot:wait-message>
      Suppression en cours...
    </template>

    <template v-slot:success-modal-body>
      <div class="modal-header border-bottom-0 flex-column align-items-center">
        <p>
          <i class="fe fe-check-circle fg-success big-icon"></i>
        </p>
        <p class="text-center">
          L'espace de dépôt <strong>"{{ control.title }}"</strong> à bien été supprimé.
        </p>
      </div>
      <div class="modal-footer border-top-0 d-flex justify-content-center">
        <button type="button"
                class="btn btn-primary"
                @click="goHome"
        >
          < Revenir à l'accueil
        </button>
      </div>
    </template>

  </modal-flow>
</template>

<script>
import backendUrls from '../utils/backend.js'
import ModalFlow from '../utils/ModalFlow'
import Vue from 'vue'

export default Vue.extend({
  props: {
    control: Object,
  },
  components: {
    ModalFlow,
  },
  methods: {
    start() {
      console.debug('outer start!')
      this.$refs.modalFlow.start()
    },
    goHome() {
      window.location.assign('/accueil')
    },
    callDeleteControlAPI() {
      const url = backendUrls.deleteControl(this.control.id)
      return Vue.axios.post(url)
    },
  },
})
</script>

<style scoped>

</style>
