<template>
  <div>
    <div class="card-header pl-0">
      <button type="button" class="btn btn-sm btn-success mr-2" style="cursor: Text;" disabled>Etape 1/3: Créer le questionnaire<i class="fa fa-angle-double-right ml-4"></i></button>
      <button type="button" class="btn btn-sm btn-success mr-2" style="cursor: Text;">Etape 2/3: Ajouter des questions<i class="fa fa-angle-double-right ml-4"></button>
      <button type="button" class="btn btn-sm btn-outline-primary mr-2" style="cursor: Text;" disabled>Etape 3/3: Aperçu avant publication<i class="fa fe fe-check ml-4"></button>
    </div>
    <div class="alert alert-icon alert-primary alert-dismissible" role="alert">
      <i class="fe fe-bell mr-2" aria-hidden="true"></i>
      <button type="button" class="close" data-dismiss="alert"></button>
      A cette étape, vous pouvez créer votre questionnaire en ajoutant des thèmes,
      des questions et des annexes à vos questions.
    </div>
    <form @submit.prevent="createBody">
      <div class="card" v-for="(theme, themeIndex) in body"> <!-- Card for each theme-->
        <div class="card-status card-status-top bg-blue">
        </div>

        <div class="card-header">
          <label v-bind:for="'theme' + (themeIndex + 1)" class="form-label-h3">
            <h3 class="card-title">{{themeIndex + 1}}.</h3>
          </label>
          <input class="form-control form-control-h3"
                 placeholder="Ecrivez un thème ici"
                 type="text"
                 v-bind:id="'theme' + (themeIndex + 1)"
                 v-model="body[themeIndex].title"
                 oninvalid="this.setCustomValidity('Veuillez remplir ou supprimer les thèmes vides.')"
                 oninput="this.setCustomValidity('')"
                 required>
          <span>
            <confirm-modal :id="'deleteThemeConfirmModal' + themeIndex"
                           title="Confirmer la suppression de ce thème"
                           confirm-button="Oui, supprimer"
                           cancel-button="Non, retour"
                           @confirm="deleteTheme(themeIndex)"
            >
              <p>
                <span v-if="body[themeIndex].questions.length === 1">
                  La question associée à ce thème sera également supprimée.
                </span>
                <span v-else>
                  Les {{ body[themeIndex].questions.length }} questions associées à ce thème seront également supprimées.
                </span>
              </p>
            </confirm-modal>

            <a v-if="body[themeIndex].questions.length === 0"
               href="javascript:void(0)"
               @click.prevent="deleteTheme(themeIndex)"
               class="btn btn-link"
               title="Supprimer le thème"
            >
              <i class="fe fe-trash-2"></i>
            </a>
            <a v-else
               href="javascript:void(0)"
               class="btn btn-link"
               data-toggle="modal"
               :data-target="'#deleteThemeConfirmModal' + themeIndex"
            >
              <i class="fe fe-trash-2"></i>
            </a>
          </span>
        </div>

        <div v-for="(question, qIndex) in body[themeIndex].questions"
             class="card m-0 pt-2"> <!-- Card for each question -->
          <div class="card-header border-0">
            <label v-bind:for="'question' + (themeIndex + 1) + '.' + (qIndex + 1)">
              <span class="stamp stamp-md bg-blue mr-3" style="cursor: pointer">
                {{ themeIndex + 1 }}.{{ qIndex + 1 }}
              </span>
            </label>
            <textarea class="form-control"
                      placeholder="Ecrivez une question ici"
                      rows="4"
                      v-bind:id="'question' + (themeIndex + 1) + '.' + (qIndex + 1)"
                      v-model="body[themeIndex].questions[qIndex].description"
                      oninvalid="this.setCustomValidity('Veuillez remplir ou supprimer les questions vides.')"
                      oninput="this.setCustomValidity('')"
                      required>
            </textarea>

            <span>
              <a href="javascript:void(0)" @click.prevent="deleteQuestion(themeIndex, qIndex)" class="btn btn-link" title="Supprimer la question">
                <i class="fe fe-trash-2"></i>
              </a>
            </span>
            <question-file-upload :question-id="question.id"></question-file-upload>
          </div>
          <question-file-list :question-number="(themeIndex + 1) + '.' + (qIndex + 1)" :question-id="question.id"></question-file-list>
        </div>


        <div class="card-footer">
          <a href="javascript:void(0)" @click.prevent="addQuestion(themeIndex)" class="btn btn-primary" title="Ajouter une question">
            <i class="fe fe-plus"></i> Ajouter une question
          </a>
        </div>
      </div>

      <div class="card">
        <div class="card-footer">
          <div class="card-status card-status-top bg-blue">
          </div>
          <a href="javascript:void(0)" @click="addTheme()" class="btn btn-primary" title="Ajouter un thème">
            <i class="fe fe-plus"></i>Ajouter un thème
          </a>
        </div>
      </div>

      <div class="text-right">
        <button type="submit" @click.prevent="back()" class="btn btn-secondary ml-auto">
          < Retour
        </button>
        <button type="submit" @click.prevent="saveDraft" class="btn btn-primary">Enregistrer le brouillon</button>
        <button type="submit" class="btn btn-secondary ml-auto">
          Suivant >
        </button>
      </div>

    </form>

  </div>
</template>

<script>
  import Vue from "vue";
  import EventBus from '../events'
  import ConfirmModal from "../utils/ConfirmModal"
  import QuestionFileList from "./QuestionFileList"
  import QuestionFileUpload from "./QuestionFileUpload"

  export default Vue.extend({
    data() {
      return {
        body: [
          {
            title: "",
            questions: [
              {description: ""},
            ]
          }
        ],
        'errors': [],
      }
    },
    components: {
      ConfirmModal,
      QuestionFileList,
      QuestionFileUpload,
    },
    mounted() {
      let loadBody = function (data) {
        console.debug('QuestionnaireBodyCreate loadBody', data);
        // Empty old themes
        this.body = []
        // Replace with new themes
        data.themes.forEach(theme => {
          console.debug('theme', theme)
          this.body.push(theme)
        })
      }.bind(this)

      this.$parent.$on('questionnaire-loaded', function(data) {
        loadBody(data);
        EventBus.$emit('question-files-changed');
      })
      this.$parent.$on('questionnaire-updated', function(data) {
        loadBody(data);
        EventBus.$emit('question-files-changed');
      })
    },
    methods: {
      back: function () {
        this.$emit('back');
      },
      createBody: function () {
        console.debug('QuestionnaireBodyCreate createBody', this.body)
        this.$emit('body-created', this.body)
      },
      addQuestion: function (themeIndex) {
        console.debug('addQuestion', themeIndex)
        this.body[themeIndex].questions.push({ description: ""});
      },
      addTheme: function () {
        console.debug('addTheme')
        this.body.push({ title: "", questions: [{description: ""}]})
      },
      deleteQuestion: function (themeIndex, qIndex) {
        this.body[themeIndex].questions.splice(qIndex, 1);
      },
      deleteTheme: function (themeIndex) {
        this.body.splice(themeIndex, 1);
      },
      saveDraft(event) {
        console.debug('save draft', event)
        if (!event.target.form.reportValidity()) {
          return
        }
        this.$emit('save-draft', this.body)
      }
    }
  });
</script>

<style>
</style>
