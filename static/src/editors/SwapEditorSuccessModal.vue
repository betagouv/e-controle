<template>
  <empty-modal no-close="true">
    <div class="modal-header border-bottom-0 flex-column align-items-center">
      <p>
        <i class="fe fe-check-circle fg-success big-icon"></i>
      </p>
      <h4 class="text-center">
        Les droits de rédaction ont été transférés !
      </h4>
    </div>
    <div class="modal-body text-center">
      <p>
        Pour devenir rédacteur de ce questionnaire à nouveau, il faudra que
        votre collègue transfère ou libère les droits de rédaction.
      </p>
    </div>
    <div class="modal-footer border-top-0 d-flex justify-content-center">
      <a  :href="homeUrl" role="button" class="btn btn-primary">
        < Revenir à l'accueil
      </a>
    </div>
  </empty-modal>
</template>

<script>
import Vue from 'vue'
import EmptyModal from '../utils/EmptyModal'
import backendUrls from '../utils/backend.js'

export default Vue.extend({
  props: ['questionnaire'],
  data: function() {
    return {
      homeUrl: backendUrls.home(),
    }
  },
  components: {
    EmptyModal,
  },
})
</script>
