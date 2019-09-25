<template>
  <div>

    <wizard active="3" @previous="back()">
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
          <button type="submit" @click.prevent="saveDraft" class="btn btn-primary">Enregistrer le brouillon</button>
          <button type="submit"
                  data-toggle="modal"
                  data-target="#saveQuestionnaireConfirmModal"
                  class="btn btn-primary ml-auto"
                  title="Publier le questionnaire à l'organisme interrogé">
            Publier
          </button>
        </div>

        <confirm-modal id="saveQuestionnaireConfirmModal"
                       title="Confirmer la publication"
                       confirm-button="Oui, j'ai compris"
                       cancel-button="Retour"
                       @confirm="done()"
        >
          <p>
            En publiant ce questionnaire, il sera visible par l'organisme interrogé et vous ne pourrez plus le modifier.
          </p>

          <info-bar>
            Pensez à informer l'organisme interrogé que vous
            avez publié ce nouveau questionnaire et qu'il est disponible à cette adresse :
            <p> https://e-controle-beta.ccomptes.fr </p>
          </info-bar>

          <info-bar>
              Si des réponses sont déposées par l'organisme interrogé, l'équipe de contrôle recevra un email d'information dès le lendemain à huit heures.
          </info-bar>

        </confirm-modal>
      </div>
    </div>

  </div>
</template>

<script>
  import Vue from "vue"
  import ConfirmModal from "../utils/ConfirmModal"
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
      done: function () {
        this.$emit('save-questionnaire')
      },
      saveDraft(event) {
        console.debug('save draft', event)
        this.$emit('save-draft')
      },
    },
    components: {
      ConfirmModal,
      QuestionnaireDetailForPreview,
      InfoBar,
      Wizard,
    }
  });
</script>

<style>
</style>
