<template>
  <div>

    <wizard :active-step-number="3"
            :step-titles="['Renseigner l\'introduction', 'Ajouter des questions', 'Aperçu avant publication']"
            @previous="back">
    </wizard>

    <div class="card">
      <div class="card-header">
        <div class="card-title">Etape 3 : Aperçu avant publication</div>
      </div>
      <div class="card-body pb-6">
        <questionnaire-detail-for-preview v-bind:questionnaire="currentQuestionnaire">
        </questionnaire-detail-for-preview>
        <div class="text-right">
          <button type="submit" @click.prevent="back()" class="btn btn-secondary ml-auto">
            < Retour
          </button>
          <button id="saveDraftFromPreviewButton" type="submit" @click.prevent="saveDraft" class="btn btn-primary">
            <i class="fe fe-save mr-1"></i>
            Enregistrer le brouillon
          </button>
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
import Wizard from '../utils/Wizard'

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
    const updateQuestionnaire = function (data) {
      // Use Vue's $set to make the properties reactive.
      for (const [key, value] of Object.entries(data)) {
        this.$set(this.questionnaire, key, value)
      }
    }.bind(this)

    this.$parent.$on('questionnaire-updated', data => {
      console.debug('new questionnaire', data)
      updateQuestionnaire(data)
    })

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
    back: function(clickedStep) {
      this.$emit('back', clickedStep)
    },
    publish: function() {
      this.$emit('publish-questionnaire')
    },
    saveDraft(event) {
      console.debug('save draft', event)
      this.publishError = undefined
      this.$emit('save-draft')
    },
  },
  components: {
    PublishConfirmModal,
    QuestionnaireDetailForPreview,
    Wizard,
  },
})
</script>

<style>
</style>
