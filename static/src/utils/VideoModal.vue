<template>
    <div class="modal" tabindex="-1" role="dialog">
      <div class="modal-dialog modal-video" role="document">
        <div class="modal-content">
          <div class="modal-header border-bottom-0">
            <button type="button"
                    class="close"
                    data-dismiss="modal"
                    aria-label="Close">
            </button>
          </div>
          <div class="modal-body">
              <video width="960" height="540" controls>
                <source v-for="videoVersion in videoVersions"
                        :key="videoVersion.type"
                        :src="videoVersion.url"
                        :type="videoVersion.type">
                La vidéo ne fonctionne pas avec votre navigateur.
              </video>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
import Vue from 'vue'

export default Vue.extend({
  props: {
    videoVersions: Array,
  },
})
</script>

<style scoped>
  .modal-video {
      width: 1000px;
      max-width: 100%;
      margin: 2% auto;
  }
</style>
