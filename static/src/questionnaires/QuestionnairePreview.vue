<template>
  <div class="card">
    <div class="card-header">
      <div class="card-title">Etape 3 : Aperçu avant publication</div>
    </div>
    <div class="card-body pb-6">
      <div class="preview mb-4">
        <questionnaire-detail-for-preview v-bind:questionnaire="questionnaire">
        </questionnaire-detail-for-preview>
      </div>
      <div class="text-right">
        <button type="submit" @click.prevent="back()" class="btn btn-secondary ml-auto">
          < Retour
        </button>
        <button type="submit" @click.prevent="saveDraft" class="btn btn-primary">
          <i class="fe fe-save"></i>
          Enregistrer le brouillon
        </button>
        <button type="submit"
                data-toggle="modal"
                data-target="#publishQuestionnaireModal"
                class="btn btn-success ml-auto"
                title="Publier le questionnaire à l'organisme interrogé">
          <i class="fa fa-rocket"></i>
          Publier
        </button>
      </div>

      <publish-questionnaire-modal id="publishQuestionnaireModal">
      </publish-questionnaire-modal>

    </div>
  </div>
</template>

<script>
  import Vue from "vue"
  import InfoBar from "../utils/InfoBar"
  import PublishQuestionnaireModal from "./PublishQuestionnaireModal"
  import QuestionnaireDetailForPreview from "./QuestionnaireDetailForPreview"

  export default Vue.extend({
    data: function () {
      return {
        questionnaire: {},
      }
    },
    mounted() {
      let updateQuestionnaire = function (data) {
        // Use Vue's $set to make the properties reactive.
        for (const [key, value] of Object.entries(data)) {
          this.$set(this.questionnaire, key, value)
        }
      }.bind(this);

      this.$parent.$on('questionnaire-updated', function (data) {
        console.debug('new questionnaire', data);
        updateQuestionnaire(data);
      });
    },
    methods: {
      back: function () {
        this.$emit('back')
      },
      done: function () {
        this.$emit('save-questionnaire')
      },
      saveDraft(event) {
        console.debug('save draft', event)
        this.$emit('save-draft')
      },
    },
    components: {
      InfoBar,
      PublishQuestionnaireModal,
      QuestionnaireDetailForPreview,
    }
  });
</script>

<style>
</style>
