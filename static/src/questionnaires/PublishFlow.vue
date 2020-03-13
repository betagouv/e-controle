<template>
  <modal-flow ref="modalFlow" :action-function="publishFunction">
    <template v-slot:confirm-modal-form>
      <div class="modal-header border-bottom-0">
        <h4 class="modal-title">
          Vous y êtes presque! En cochant ces mentions, vous êtes informés que :
        </h4>
      </div>

      <div class="modal-body">
        <label class="custom-control custom-checkbox">
          <input type="checkbox"
                  class="custom-control-input"
                  required>
          <span class="custom-control-label">
            Le questionnaire ne pourra plus être modifié
          </span>
        </label>
        <label class="custom-control custom-checkbox">
          <input type="checkbox"
                  class="custom-control-input"
                  required>
          <span class="custom-control-label">
            Le questionnaire deviendra visible par l'organisme interrogé
          </span>
        </label>
        <label class="custom-control custom-checkbox">
          <input type="checkbox"
                  class="custom-control-input"
                  required>
          <span class="custom-control-label">
            Vous devrez informer l'organisme interrogé
          </span>
        </label>
      </div>

      <div class="modal-footer border-top-0">
        <button type="button"
                class="btn btn-secondary"
                data-dismiss="modal"
                title="J'ai encore des modifications à faire"
        >
          J'ai encore des modifications à faire
        </button>
        <button type="submit"
                class="btn btn-primary"
                title="Publier le questionnaire"
        >
          <i class="fa fa-rocket mr-1"></i>
          Publier le questionnaire
        </button>
      </div>
    </template>

    <template v-slot:wait-message>
      Questionnaire en cours de publication ...
    </template>

    <template v-slot:error-message>
      <div>
        Le questionnaire n'a pas pu être publié. Vous pouvez réessayer.
      </div>
      <div>
        Si l'erreur persiste, vous pouvez contacter
        <a :href="'mailto:' + config.support_team_email + '?subject=Erreur lors de la publication :' + JSON.stringify($refs.modalFlow.error)"
            class="text-nowrap"
            target="_blank"
        >
          {{ config.support_team_email }}
        </a>
        , et indiquer l'erreur suivante :
      </div>
      <div>
        {{ $refs.modalFlow.error }}
      </div>
    </template>

    <template v-slot:success-modal-body>
      <div class="modal-header border-bottom-0 flex-column align-items-center">
        <p>
          <i class="fe fe-check-circle fg-success big-icon"></i>
        </p>
        <h4 class="text-center">
          Bravo, votre questionnaire est publié!
        </h4>
      </div>
      <div class="modal-body text-center">
        <p>
          Si des réponses sont déposées par l'organisme interrogé, vous recevrez un email de
          notification dès le lendemain 8 heures.
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
import backend from '../utils/backend'
import { mapFields } from 'vuex-map-fields'
import ModalFlow from '../utils/ModalFlow'
import Vue from 'vue'

export default Vue.extend({
  components: {
    ModalFlow,
  },
  props: {
    controlId: Number,
    publishFunction: Function,
    // Pass window dependency for testing
    window: {
      default: () => window,
    },
  },
  computed: {
    ...mapFields([
      'config',
    ]),
  },
  methods: {
    start() {
      console.debug('outer start!')
      this.$refs.modalFlow.start()
    },
    goHome() {
      this.window.location.href = backend['control-detail'](this.controlId)
    },
  },
})
</script>

<style scoped>

</style>
