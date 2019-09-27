<template>
  <div>

    <wizard :active-step-number="3"
            :step-titles="['Renseigner l\'introduction', 'Ajouter des questions', 'Aperçu avant publication']"
            @previous="back()">
    </wizard>

    <div class="card">
      <div class="card-header">
        <div class="card-title">Etape 3 : Aperçu avant publication</div>
      </div>
      <div class="card-body pb-6">
        <questionnaire-detail-for-preview v-bind:questionnaire="questionnaire">
        </questionnaire-detail-for-preview>
        <div class="text-right">
          <button type="submit" @click.prevent="back()" class="btn btn-secondary ml-auto">
            < Retour
          </button>
          <button type="submit" @click.prevent="saveDraft" class="btn btn-primary">
            <i class="fe fe-save mr-1"></i>
            Enregistrer le brouillon
          </button>
          <button id="publishButton"
                  type="submit"
                  data-toggle="modal"
                  data-target="#publishConfirmModal"
                  class="btn btn-primary ml-5"
                  title="Publier le questionnaire à l'organisme interrogé">
            <i class="fa fa-rocket mr-1"></i>
            Publier
          </button>
        </div>

        <publish-confirm-modal id="publishConfirmModal"
                               @confirm="publish()"
        >
        </publish-confirm-modal>
      </div>
    </div>

  </div>
</template>

<script>
  import Vue from "vue"
  import PublishConfirmModal from './PublishConfirmModal'
  import QuestionnaireDetailForPreview from "./QuestionnaireDetailForPreview"
  import InfoBar from "../utils/InfoBar"
  import Wizard from "../utils/Wizard"

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
      publish: function () {
        this.$emit('publish-questionnaire')
      },
      saveDraft(event) {
        console.debug('save draft', event)
        this.$emit('save-draft')
      },
    },
    components: {
      PublishConfirmModal,
      QuestionnaireDetailForPreview,
      InfoBar,
      Wizard,
    }
  });
</script>

<style>
</style>
