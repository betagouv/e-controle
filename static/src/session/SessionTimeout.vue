<template>
  <div>
    <confirm-modal id="IdleSessionConfirmModal"
                   title="Votre session va bientôt expirer..."
                   confirm-button="Cliquez ici pour garder ma connexion"
                   @confirm="keepAlive()"
                   @close="keepAlive()">
      <p>
         Sans action de votre part, cette page sera déconnectée.
      </p>
    </confirm-modal>
  </div>
</template>

<script>
  import Vue from "vue"
  import ConfirmModal from "../utils/ConfirmModal"

  var timeout

  export default Vue.extend({
    components: {
      ConfirmModal
    },
    props: [
      'logoutUrl'
    ],
    methods: {
      showModal() {
        $('#IdleSessionConfirmModal').modal('show')
      },
      hideModal() {
        $('#IdleSessionConfirmModal').modal('hide')
      },
      keepAlive() {
        clearTimeout(timeout)
        this.hideModal()
        this.startSessionTimer()
      },
      startSessionTimer() {
        var expireSeconds = 60
        console.debug('Start or restart session timer')
        timeout = setTimeout(() => {
          console.debug('Idle session started')
          this.startGracePeriod()
        }, expireSeconds*1000); // JS timeout is specified in milliseconds.
      },
      startGracePeriod() {
        this.showModal()
        console.debug('Start grace period for idle session')
        timeout = setTimeout(() => {
          console.debug('End of grace period for idle session. Logout on this URL: ' + this.logoutURL)
          window.location.href = this.logoutUrl
        }, 30*1000); // 30 seconds
      }
    },
    mounted() {
      console.debug("Mounted session timout")
      this.startSessionTimer()
    }
  })
</script>
