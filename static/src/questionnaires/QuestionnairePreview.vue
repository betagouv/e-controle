<template>
  <div>
    <div class="card-header">
      <div class="card-options">
        <button type="submit" @click.prevent="saveDraft" class="btn btn-primary">Enregistrer le brouillon</button>
      </div>
    </div>
    <div class="preview">
      <questionnaire-detail v-bind:questionnaire="questionnaire">
      </questionnaire-detail>
    </div>
    <div class="text-right">
      <a href="javascript:void(0)" @click.prevent="back()" class="btn btn-link">
        < Retour
      </a>
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
      En publiant ce questionnaire, vous allez le rendre visible à l'organisme interrogé, et vous ne pourrez plus le modifier.
    </confirm-modal>

  </div>
</template>

<script>
  import Vue from "vue"
  import ConfirmModal from "../utils/ConfirmModal"
  import QuestionnaireDetail from "./QuestionnaireDetail"

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
      QuestionnaireDetail
    }
  });
</script>

<style>
</style>