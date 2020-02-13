<template>
  <confirm-modal title="Réorganiser les thèmes du questionnaire"
                 confirm-button="Ok">
    <div class="table-responsive border">
      <table class="table card-table">
        <tbody>

          <tr v-for="(theme, themeIndex) in themes"
              :key="theme.id"
              class="flex-row">
            <td>
              <div class="flex-column align-items-center">
                <button :class="{ disabled: themeIndex === 0 }"
                  class="btn btn-secondary btn-sm move-up-button"
                  role="button"
                  type="button"
                  title="Déplacer le thème vers le haut"
                  @click="moveThemeUp(themeIndex)">
                  <i class="fa fa-chevron-up"></i>
                </button>
                <div>
                  {{ themeIndex + 1 }}
                </div>
                <button :class="{ disabled: themeIndex === (themes.length - 1) }"
                  class="btn btn-secondary btn-sm move-down-button"
                  role="button"
                  type="button"
                  title="Déplacer le thème vers le bas"
                  @click="moveThemeDown(themeIndex)">
                  <i class="fa fa-chevron-down"></i>
                </button>
              <div>
            </td>
            <td class="flex-grow-1 flex-column justify-content-center">
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
