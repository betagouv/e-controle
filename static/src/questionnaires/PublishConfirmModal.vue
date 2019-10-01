<template>
  <empty-modal>
    <div class="modal-body">
      <error-bar noclose="true" v-if="error">
        <div>
          Le questionnaire n'a pas pu être publié. Vous pouvez réessayer.
        </div>
        <div>
          Si l'erreur persiste, vous pouvez contacter
          <a :href="'mailto:e-controle@beta.gouv.fr?subject=Erreur lors de la publication : ' + JSON.stringify(error)"
             class="text-nowrap"
             target="_blank"
          >
            e-controle@beta.gouv.fr
          </a>
          , et indiquer l'erreur suivante :
        </div>
        <div>
          {{ error }}
        </div>
      </error-bar>
      <form @submit.prevent="done">

        <div class="modal-header border-bottom-0">
          <h4 class="modal-title">Vous y êtes presque! En cochant ces mentions, vous êtes informés que :</h4>
          <button type="button"
                  class="close"
                  data-dismiss="modal"
                  aria-label="Close">
          </button>
        </div>

        <div class="modal-body">
          <div>
            <input type="checkbox"
                   name="save-questionnaire-checkbox-1"
                   id="save-questionnaire-checkbox-1"
                   required>
            <label for="save-questionnaire-checkbox-1">
              Le questionnaire ne pourra plus être modifié
            </label>
          </div>
          <div>
            <input type="checkbox"
                   name="save-questionnaire-checkbox-2"
                   id="save-questionnaire-checkbox-2"
                   required>
            <label for="save-questionnaire-checkbox-2">
              Le questionnaire deviendra visible par l'organisme interrogé
            </label>
          </div>
           <div>
            <input type="checkbox"
                   name="save-questionnaire-checkbox-3"
                   id="save-questionnaire-checkbox-3"
                   required>
            <label for="save-questionnaire-checkbox-3">
              Vous devrez informer l'organisme interrogé
            </label>
          </div>
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

      </form>
    </div>
  </empty-modal>

</template>

<script>
  import EmptyModal from "../utils/EmptyModal"
  import ErrorBar from '../utils/ErrorBar'
  import Vue from 'vue'

  export default Vue.extend({
    components: {
      EmptyModal,
      ErrorBar,
    },
    props: ['error'],
    methods: {
      done: function(event) {
        this.$emit('confirm')
        // We hide the modal programmatically rather than using data-dismiss on the button, because it dismisses before
        // the form validation step.
        $(this.$el).modal('hide')
      },
    },
  })
</script>

<style scoped>

</style>
