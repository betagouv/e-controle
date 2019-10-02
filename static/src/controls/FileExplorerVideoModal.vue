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
            <center>
              <video width="960" height="540" controls>
                <source :src="videoUrl" :type='videoType'>
                  La vidéo ne fonctionne pas avec votre navigateur.
              </video>
            </center>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
  import Vue from 'vue'

  export default Vue.extend({
    props: {
      videoUrl: String,
      videoType: String
    }
  })
</script>

<style scoped></style>
