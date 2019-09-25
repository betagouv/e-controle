<template>
  <empty-modal>
    <form @submit.prevent="done">

      <div class="modal-header border-bottom-0">
        <h5 class="modal-title">Vous y êtes presque! En cochant ces mentions, vous êtes informés que :</h5>
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
                 v-model="checkbox1"
                 required>
          <label for="save-questionnaire-checkbox-1">
            Le questionnaire ne pourra plus être modifié
          </label>
        </div>
        <div>
          <input type="checkbox"
                 name="save-questionnaire-checkbox-2"
                 id="save-questionnaire-checkbox-2"
                 v-model="checkbox2"
                 required>
          <label for="save-questionnaire-checkbox-2">
            Le questionnaire deviendra visible par l'organisme interrogé
          </label>
        </div>
      </div>

      <div class="modal-footer border-top-0">
        <button type="submit"
                class="btn btn-primary"
                title="Publier le questionnaire"
        >
          <i class="fa fa-rocket mr-1"></i>
          Publier le questionnaire
        </button>
        <button type="button"
                class="btn btn-secondary"
                data-dismiss="modal"
                title="J'ai encore des modifications à faire"
        >
          J'ai encore des modifications à faire
        </button>
      </div>

    </form>
  </empty-modal>

</template>

<script>
  import EmptyModal from "../utils/EmptyModal"
  import Vue from 'vue'

  export default Vue.extend({
    components: {
      EmptyModal
    },
    data: function() {
      return {
        checkbox1 : false,
        checkbox2 : false,
      }
    },
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