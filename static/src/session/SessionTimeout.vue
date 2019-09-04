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
  import VueAxios from "vue-axios"

  Vue.use(VueAxios, axios)

  var timeout

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
        let expireMs = this.expireSeconds - this.expireSeconds * 0.1
        expireMs = expireMs*1000
        return expireMs
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
        Vue.axios.get('/api/session/keep-alive').then((response) => {
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
        }, 30*1000); // 30 seconds
      }
    },
    mounted() {
      console.debug("Mounted session timeout")
      this.startSessionTimer()
    }
  })
</script>
