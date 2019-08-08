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
  import IdleVue from 'idle-vue'

  import ConfirmModal from "../utils/ConfirmModal"

  const eventsHub = new Vue()
  var timeout

  Vue.use(IdleVue, {
    eventEmitter: eventsHub,
    idleTime: 4*60*60*1000 // 4 hours
  })

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
      }
    },
    onIdle() {
      this.showModal()
      console.debug('Detected idle session.')
      timeout = setTimeout(() => {
        console.debug('Idle session: end of grace period. Logout on this URL: ' + this.logoutURL)
        window.location.href = this.logoutUrl
      }, 30*1000); // 30 seconds
    }
  })

</script>
