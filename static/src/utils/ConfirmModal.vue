<template>
  <div class="modal" tabindex="-1" role="dialog">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">{{ title }}</h5>
          <button type="button"
                  class="close"
                  data-dismiss="modal"
                  aria-label="Close"
                  @click="closeModal">
          </button>
        </div>
        <div class="modal-body">
          <slot></slot>
        </div>
        <div class="modal-footer">
          <button v-if="confirmButton" type="button" class="btn btn-primary"
                  data-dismiss="modal"
                  @click="confirmClicked"
          >
            {{ confirmButton }}
          </button>
          <button v-if="cancelButton" type="button" class="btn btn-secondary"
                  data-dismiss="modal"
                  @click="cancelClicked"
          >
            {{ cancelButton }}
          </button>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
  import Vue from "vue"

  export default Vue.extend({
    props: [
        'cancel-button',
        'confirm-button',
        'title'
    ],
    methods: {
      confirmClicked () {
        this.$emit('confirm')
      },
      cancelClicked () {
        this.$emit('cancel')
      },
      closeModal () {
        this.$emit('close')
      },
    }
  })

</script>

<style></style>
