<template>
  <confirm-modal title="Réorganiser les thèmes du questionnaire"
                 confirm-button="Ok">
    <div class="table-responsive border">
      <table class="table card-table">
        <transition-group name="theme-list" tag="tbody">

          <tr v-for="(theme, themeIndex) in themes"
              :id="'move-themes-modal-theme-' + themeIndex"
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

        </transition-group>
      </table>
    </div>
  </confirm-modal>
</template>

<script>
import axios from 'axios'
import backendUrls from '../utils/backend'
import ConfirmModal from '../utils/ConfirmModal'
import { mapFields } from 'vuex-map-fields'
import Vue from 'vue'
import SwapMixin from '../utils/SwapMixin'

export default Vue.extend({
  components: {
    ConfirmModal,
  },
  mixins: [
    SwapMixin,
  ],
  computed: {
    ...mapFields([
      'currentQuestionnaire.themes',
    ]),
  },
  methods: {
    moveThemeUp(themeIndex) {
      const array = this.themes
      const selectedJqueryElement = $('#move-themes-modal-theme-' + themeIndex)
      this.swapMixin_moveItemUp(array, themeIndex, selectedJqueryElement)
      this.saveThemeOrder(themeIndex)
      this.saveThemeOrder(themeIndex - 1)
    },
    moveThemeDown(themeIndex) {
      const array = this.themes
      const selectedJqueryElement = $('#move-themes-modal-theme-' + themeIndex)
      this.swapMixin_moveItemDown(array, themeIndex, selectedJqueryElement)
      this.saveThemeOrder(themeIndex)
      this.saveThemeOrder(themeIndex + 1)
    },
    saveThemeOrder(themeIndex) {
      const theme = this.themes[themeIndex]
      return axios.put(
        backendUrls.theme(theme.id),
        {
          title: theme.title, // title is required, so add it even though we're not changing it
          order: theme.order,
        })
      // Todo deal with errors
    },
  },
})
</script>

<style>
.theme-list-move {
  transition: transform 1s; /* same as SwapMixin.ANIMATION_DURATION_SECONDS */
}
.theme-list-move.selected {
  z-index: 999;
  background-color: var(--azure-lightest);
}
</style>
