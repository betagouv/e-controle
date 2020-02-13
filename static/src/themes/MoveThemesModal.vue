<template>
  <confirm-modal title="Réorganiser les thèmes du questionnaire"
                 confirm-button="Ok">
    <div class="table-responsive border">
      <table class="table card-table">
        <tbody>

          <tr v-for="theme in themes"
              :key="theme.id"
              class="flex-row">
            <td>
              {{ theme.order + 1 }}
            </td>
            <td>
              <i class="fa fa-grip-lines"></i>
            </td>
            <td class="flex-grow-1">
              {{ theme.title }}
            </td>
          </tr>

        </tbody>
      </table>
    </div>
  </confirm-modal>
</template>

<script>
import ConfirmModal from '../utils/ConfirmModal'
import { mapFields } from 'vuex-map-fields'
import Vue from 'vue'

export default Vue.extend({
  components: {
    ConfirmModal,
  },
  computed: {
    ...mapFields([
      'currentQuestionnaire.themes',
    ]),
  },
})
</script>
