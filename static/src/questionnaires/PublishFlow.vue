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
          <i class="fa fa-chevron-left mr-2"></i>
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
        <a :href="'mailto:' + config.support_team_email +
                  '?subject=Erreur lors de la publication : ' +
                  $refs.modalFlow.error.message"
            class="text-nowrap"
            target="_blank"
            rel="noopener noreferrer"
        >
          {{ config.support_team_email }}
        </a>
        , et indiquer l'erreur suivante :
      </div>
      <div>
        {{ $refs.modalFlow.error.message }}
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
        <div class="mt-5">
            <p>Pensez à informer l'organisme contrôlé.</p>
            <p>Si des réponses sont déposées par l'organisme interrogé, vous recevrez un email de
          notification dès le lendemain 8 heures.</p>
        </div>
      </div>
      <div class="modal-body text-center">
        <div class="mt-5 flex-row justify-content-center">
          <button type="button"
            class="btn btn-primary ml-2"
            @click="goHome"
          >
            <i class="fa fa-chevron-left mr-2"></i>
            Revenir à l'accueil
          </button>
          <a class="btn btn-primary ml-2"
              :href="'mailto:' +
                    '?subject=Questionnaire publié' +
                    '&body=' + emailBody"
              target="_blank"
              rel="noopener noreferrer"
          >
            Créer un mail pour l'informer
          </a>
        </div>
      </div>
    </template>

  </modal-flow>
</template>

<script>
import backend from '../utils/backend'
import { mapFields } from 'vuex-map-fields'
import { mapState } from 'vuex'
import ModalFlow from '../utils/ModalFlow'
import Vue from 'vue'

export default Vue.extend({
  components: {
    ModalFlow,
  },
  props: {
    questionnaire: Object,
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
    ...mapState({
      controls: 'controls',
    }),
    emailBody: function() {
      const currentControl = this.controls.find(control => control.id === this.questionnaire.control)
      const expiryDateString = this.questionnaire.end_date === null ? '' : ' La date limite de réponse est le' + this.questionnaire.end_date + '.'

      if (currentControl) {
        const newline = '%0d%0a'
        return `Bonjour,${newline}${newline}Un nouveau questionnaire vient d'être ajouté au contrôle ${currentControl.title}. Il s'agit du questionnaire numéro ${this.questionnaire.id} : ${this.questionnaire.title}.${expiryDateString}${newline}${newline}Nous vous invitons à vous connecter à e-contrôle pour le voir, au lien ci-dessous :${newline}${newline}https://e-controle-beta.ccomptes.fr${newline}${newline}Cordialement,`
      }

      return ''
    },
  },
  methods: {
    start() {
      console.debug('outer start!')
      this.$refs.modalFlow.start()
    },
    goHome() {
      this.window.location.href = backend['control-detail'](this.questionnaire.control)
    },
  },
})
</script>

<style scoped>

</style>
