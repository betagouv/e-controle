<template>
  <div>
    <div class="card">
      <div class="card-header">
        <div class="card-title">Etape 3 : Aperçu avant publication</div>
      </div>
      <div class="card-body pb-6">
        <questionnaire-detail-for-preview v-bind:questionnaire="currentQuestionnaire">
        </questionnaire-detail-for-preview>
        <div class="text-right">
          <button id="publishButton"
                  ref="publishButton"
                  @click="showPublishConfirmModal()"
                  class="btn btn-primary ml-5"
                  title="Publier le questionnaire à l'organisme interrogé">
            <i class="fa fa-rocket mr-1"></i>
            Publier
          </button>
        </div>

        <publish-confirm-modal ref="publishConfirmModal"
                               id="publishConfirmModal"
                               :error="publishError"
                               @confirm="publish()"
        >
        </publish-confirm-modal>
      </div>
    </div>

  </div>
</template>

<script>
import Vue from 'vue'
import { mapFields } from 'vuex-map-fields'
import PublishConfirmModal from './PublishConfirmModal'
import QuestionnaireDetailForPreview from './QuestionnaireDetailForPreview'

export default Vue.extend({
  data: function() {
    return {
      questionnaire: {},
      publishError: undefined,
    }
  },
  computed: {
    ...mapFields([
      'currentQuestionnaire',
    ]),
  },
  mounted() {
    this.$parent.$on('publish-questionnaire-error', error => {
      console.debug('got publish-questionnaire-error', error)
      this.showPublishConfirmModal()
      this.publishError = error
    })

    $(this.$refs.publishConfirmModal.$el).on('hidden.bs.modal', () => {
      this.publishError = undefined
    })
  },
  methods: {
    showPublishConfirmModal: function () {
      $(this.$refs.publishConfirmModal.$el).modal('show')
    },
    publish: function() {
      this.$emit('publish-questionnaire')
    },
  },
  components: {
    PublishConfirmModal,
    QuestionnaireDetailForPreview,
  },
})
</script>

<style>
</style>
