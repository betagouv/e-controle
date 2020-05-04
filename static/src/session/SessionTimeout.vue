<template>
  <div>
    <confirm-modal id="IdleSessionConfirmModal"
                   title="Votre session va bientôt expirer..."
                   confirm-button="Garder ma session active"
                   @confirm="keepAlive()"
                   @close="keepAlive()">
      <p>
         Sans action de votre part, votre session va expirer.
      </p>
    </confirm-modal>
  </div>
</template>

<script>
  import axios from "axios"
  import ConfirmModal from "../utils/ConfirmModal"
  import Vue from "vue"

  var timeout
  var gracePeriodMs = 30*1000 // In milliseconds. How long the warning modal stays opened.

  export default Vue.extend({
    components: {
      ConfirmModal
    },
    props: [
      'logoutUrl',
      'expireSeconds'
    ],
    computed: {
      frontendExpireMs() {
        // The frontend expire timeout is 10% less that the backend timout.
        // Also, JS timeout is specified in milliseconds.
        let frontendExpire = this.expireSeconds - this.expireSeconds*0.1
        frontendExpire = frontendExpire*1000
        return frontendExpire
      }
    },
    methods: {
      showModal() {
        $('#IdleSessionConfirmModal').modal('show')
      },
      keepAlive() {
        clearTimeout(timeout)
        this.startSessionTimer()
        this.keepServerAlive()
      },
      keepServerAlive() {
        axios.get('/api/session/keep-alive').then((response) => {
          console.debug('Keep server alive')
        })
      },
      startSessionTimer() {
        console.debug('Start or restart session timer: ' + this.frontendExpireMs)
        timeout = setTimeout(() => {
          console.debug('Idle session started')
          this.startGracePeriod()
        }, this.frontendExpireMs);
      },
      startGracePeriod() {
        this.showModal()
        console.debug('Start grace period for idle session')
        timeout = setTimeout(() => {
          console.debug('End of grace period for idle session. Logout on this URL: ' + this.logoutURL)
          window.location.href = this.logoutUrl
        }, gracePeriodMs);
      }
    },
    mounted() {
      console.debug("Mounted session timeout component")
      this.startSessionTimer()
    }
  })
</script>
