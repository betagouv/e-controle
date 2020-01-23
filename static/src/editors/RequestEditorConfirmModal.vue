<template>
  <empty-modal :no-close="true">
    <div class="modal-body">
      <form @submit.prevent="confirm">

        <div class="modal-header border-bottom-0">
          <h4 class="modal-title">
            Vous êtes sur le point de forcer le transfert des droits
            de ce questionnaire, en conséquence :
          </h4>
        </div>

        <div class="modal-body">
          <div class="flex-row">
            <input class="mt-2"
                   type="checkbox"
                   name="become-editor-checkbox-1"
                   id="become-editor-checkbox-1"
                   required>
            <label class="ml-2" for="become-editor-checkbox-1">
              Les modifications non enregistrées de votre collègue seront perdues.
            </label>
          </div>
          <div class="flex-row">
            <input class="mt-2"
                   type="checkbox"
                   name="become-editor-checkbox-2"
                   id="become-editor-checkbox-2"
                   required>
            <label class="ml-2" for="become-editor-checkbox-2">
              Pour que d'autres puissent modifier ce questionnaire,
              vous devrez libérer ou transférer les droits de rédaction.
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
                  class="btn btn-primary"
                  title="Forcer le transfert"
          >
            <i class="fa fa-exchange-alt mr-1"></i>
            Forcer le transfert
          </button>
        </div>

      </form>
    </div>
  </empty-modal>

</template>

<script>
import { mapFields } from 'vuex-map-fields'
import Vuex from 'vuex'
import EmptyModal from '../utils/EmptyModal'
import Vue from 'vue'

Vue.use(Vuex)

export default Vue.extend({
  components: {
    EmptyModal,
  },
  computed: {
    ...mapFields(['sessionUser']),
  },
  methods: {
    confirm() {
      this.$emit('confirm')
    },
  },
})
</script>

<style scoped>

</style>
