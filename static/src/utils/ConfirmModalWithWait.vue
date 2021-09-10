<template>
  <empty-modal :no-close="noClose">
    <form>
      <div class="modal-header border-bottom-0">
        <h5 class="modal-title">{{ title }}</h5>
        <button
          v-if="!noClose"
          type="button"
          class="close"
          data-dismiss="modal"
          aria-label="Close"
          @click="closeModal"
        ></button>
      </div>
      <div class="modal-body">
        <error-bar v-if="errorMessage">
          {{ errorMessage }}
        </error-bar>
        <slot></slot>
      </div>
      <div class="modal-footer border-top-0">
        <button
          v-if="confirmButton"
          type="submit"
          class="btn btn-primary"
          @click.prevent="confirmClicked"
          :class="{ 'btn-loading': processing }"
        >
          {{ confirmButton }}
        </button>
        <button
          v-if="cancelButton"
          type="button"
          class="btn btn-secondary"
          data-dismiss="modal"
          @click="cancelClicked"
        >
          {{ cancelButton }}
        </button>
      </div>
    </form>
  </empty-modal>
</template>

<script>
import EmptyModal from "./EmptyModal";
import ErrorBar from "./ErrorBar";
import reportValidity from "report-validity";
import Vue from "vue";

export default Vue.extend({
  props: [
    "cancel-button",
    "confirm-button",
    "no-close",
    "title",
    "submitCallback",
    "errorCallback",
    "successCallback",
  ],
  data: function () {
    return {
      errorMessage: "",
      processing: false,
    };
  },
  components: {
    EmptyModal,
    ErrorBar,
  },
  methods: {
    confirmClicked() {
      this.errorMessage = "";
      if (!this.validateForm()) {
        return;
      }

      const processingDoneCallback = (errorMessage, successMessage) => {
        if (errorMessage) {
          console.log("error!", errorMessage);
          this.errorMessage = errorMessage;
          this.processing = false;
          return;
        }
        console.debug("ConfirmModalWithWait : processing done", successMessage);
      };

      this.processing = true;
      this.$emit("confirm", processingDoneCallback);
    },
    cancelClicked() {
      this.processing = false;
      this.errorMessage = "";
      this.$emit("cancel");
    },
    closeModal() {
      this.processing = false;
      this.errorMessage = "";
      this.$emit("close");
    },
    validateForm() {
      const forms = this.$el.getElementsByTagName("form");
      if (forms.length > 0) {
        return reportValidity(forms[0]);
      }
      return true;
    },
  },
});
</script>

<style></style>
