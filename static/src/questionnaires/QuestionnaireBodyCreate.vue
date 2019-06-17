<template>
  <div>
    <form @submit.prevent="createBody">
      <div class="card-header">
        <div class="card-options">
          <button type="submit" @click.prevent="saveDraft" class="btn btn-primary">Enregistrer le brouillon</button>
        </div>
      </div>

      <div class="card" v-for="(theme, themeIndex) in body">
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

            <confirm-modal id="deleteThemeConfirmModal"
                           title="Confirmer la suppression"
                           confirm-button="Oui, supprimer"
                           cancel-button="Non, retour"
                           @confirm="deleteTheme(themeIndex)"
            >
              <p>Ce thème contient
                <span v-if="body[themeIndex].questions.length === 1">
                  une question, qui sera supprimée avec lui.
                </span>
                <span v-else>
                  {{ body[themeIndex].questions.length }} questions, qui seront supprimées avec lui.
                </span>
              </p>
              <p>
                Êtes-vous sûr.e de vouloir supprimer ce thème?
              </p>
            </confirm-modal>

            <a v-if="body[themeIndex].questions.length === 0"
               href="javascript:void(0)"
               @click.prevent="deleteTheme(themeIndex)"
               class="btn btn-link"
            >
              <i class="fe fe-trash-2"></i>Supprimer
            </a>
            <a v-else
               href="javascript:void(0)"
               class="btn btn-link"
               data-toggle="modal"
               data-target="#deleteThemeConfirmModal"
            >
              <i class="fe fe-trash-2"></i>Supprimer
            </a>
          </span>
        </div>

        <div v-for="(question, qIndex) in body[themeIndex].questions"
             class="card border-0 m-0 p-0 pb-0 pt-2 {% cycle '' 'zebra' %}">
          <div class="card-header border-1">
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
              <a href="javascript:void(0)" @click.prevent="deleteQuestion(themeIndex, qIndex)" class="btn btn-link">
                <i class="fe fe-trash-2"></i>Supprimer
              </a>
            </span>
          </div>
        </div>

        <div class="card-footer text-right">
          <a href="javascript:void(0)" @click.prevent="addQuestion(themeIndex)" class="btn btn-primary">
            <i class="fe fe-plus"></i>Ajouter une question
          </a>
        </div>

      </div>

      <div class="card">
        <div class="card-footer text-right">
          <div class="card-status card-status-top bg-blue">
          </div>
          <a href="javascript:void(0)" @click="addTheme()" class="btn btn-primary">
            <i class="fe fe-plus"></i>Ajouter un thème
          </a>
        </div>
      </div>

      <div class="text-right">
        <a href="javascript:void(0)" @click.prevent="back()" class="btn btn-link">
          < Retour
        </a>
        <button type="submit" class="btn btn-primary ml-auto">
          Prévisualiser >
        </button>
      </div>

    </form>

  </div>
</template>

<script>
  import Vue from "vue";
  import ConfirmModal from "../utils/ConfirmModal"

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
      ConfirmModal
    },
    mounted() {
      let loadBody = function (data) {
        // Empty old themes
        this.body.splice(0, this.body.length)
        // Replace with new themes
        data.themes.forEach(theme => {
          console.debug('theme', theme)
          this.body.push(theme)
        })
      }.bind(this)

      this.$parent.$on('questionnaire-loaded', function(data) {
        console.debug('new body', data);
        loadBody(data);
      })
    },
    methods: {
      back: function () {
        this.$emit('back');
      },
      createBody: function () {
        console.debug(this.body)
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
      },
    }
  });
</script>

<style>
</style>
