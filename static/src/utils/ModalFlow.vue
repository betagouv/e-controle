<!--
  A flow in three modals :
   - 1 - confirm-modal: The user clicks checkboxes (or fills whatever other form) to validate that
   they really want to take the action.<style scoped>
   - 2 - waiting-modal: the action is taken in the background (e.g. API call) while a wait message
   is displayed.
   - 3 - success-modal: the action has successfully been taken, a success modal is displayed.

   Todo : when action errors
-->
<template>
  <div>
    <empty-modal ref="confirmModal" class="confirm-modal" :no-close="true">
      <form @submit.prevent="confirmed">
        <!--
          This slot should contain the form, which when submitted will trigger the rest of the
          flow.
          Typically a title, one or more required checkboxes, a cancel button and a submit button.
        -->
        <slot name="confirm-modal-form"></slot>
      </form>
    </empty-modal>

    <empty-modal ref="waitingModal"
                 no-close="true">
      <div class="d-flex flex-column align-items-center p-8">
        <div class="m-4">
          <!--
            This slot should contain the wait message, something like "Action is happening..."
          -->
          <slot name="wait-message"></slot>
        </div>
        <div class="loader m-4"></div>
      </div>
    </empty-modal>

    <empty-modal ref="successModal"
                 no-close="true">
      <!--
        This slot should contain the success modal.
      -->
      <slot name="success-modal-body"></slot>
    </empty-modal>

  </div>
</template>

<script>
import EmptyModal from './EmptyModal'
import Vue from 'vue'

const SPINNER_DURATION_MILLIS = 2000

export default Vue.extend({
  props: {
    // The function to run once the user has confirmed they really want to take the action.
    actionFunction: Function,
  },
  components: {
    EmptyModal,
  },
  methods: {
    // Called by parent to start the flow.
    start() {
      console.debug('start!')
      $(this.$refs.confirmModal.$el).modal('show')
    },
    wait(timeMillis) {
      return new Promise((resolve) => {
        const id = setTimeout(() => {
          clearTimeout(id)
          resolve()
        }, timeMillis)
      })
    },
    confirmed() {
      console.debug('confirmed!')
      $(this.$refs.confirmModal.$el).modal('hide')
      $(this.$refs.waitingModal.$el).modal('show')

      return Promise.all([this.wait(SPINNER_DURATION_MILLIS), this.actionFunction()])
        .then(() => {
          console.debug('Done action.')
          $(this.$refs.waitingModal.$el).modal('hide')
          $(this.$refs.successModal.$el).modal('show')
        })
        .catch(error => {
          console.error('Error deleting questionnaire : ', error)
          // todo display error.
          this.$emit('error', error)
        })
    },
  },
})
</script>

<style scoped>

</style>
