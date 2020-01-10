<template>
  <div>

    <wizard :active-step-number="2"
            :step-titles="['Renseigner l\'introduction', 'Ajouter des questions', 'Aperçu avant publication']"
            @next="createBody"
            @previous="back">
    </wizard>

    <div class="card">
      <div class="card-header">
        <div class="card-title">Etape 2 : Ajouter des questions</div>
      </div>
      <div class="card-body pb-6">
        <info-bar>
          A cette étape, vous pouvez créer votre questionnaire en ajoutant des thèmes,
          des questions et des annexes à vos questions.
        </info-bar>
        <form @submit.prevent="createBody" ref="form">
          <div class="card"
               v-for="(theme, themeIndex) in body"
               :key="'theme-' + themeIndex"> <!-- Card for each theme-->
            <div class="card-status card-status-top bg-blue">
            </div>

            <div class="border-bottom">
              <div class="card-header border-0 pb-0">
                <label v-bind:for="'theme' + (themeIndex + 1)" class="form-label-h3">
                  <h3 class="card-title">{{themeIndex + 1}}.</h3>
                </label>
                <input class="form-control form-control-h3"
                       placeholder="Ecrivez un thème ici"
                       type="text"
                       maxlength="255"
                       v-bind:id="'theme' + (themeIndex + 1)"
                       v-model="body[themeIndex].title"
                       oninvalid="this.setCustomValidity('Veuillez remplir ou supprimer les thèmes vides.')"
                       oninput="this.setCustomValidity('')"
                       :aria-describedby="'theme' + (themeIndex + 1) + 'Help'"
                       required>
                <span>
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
              <div class="text-muted pb-2 pl-6" :id="'theme' + (themeIndex + 1) + 'Help'">
                Exemple : "Ressources Humaines". 255 caractères maximum.
              </div>
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
            </div>

            <div v-for="(question, qIndex) in body[themeIndex].questions"
                 class="card border-0 m-0 pt-2"
                 :key="'question-' + qIndex"> <!-- Card for each question -->
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
              <div class="card-body">
                <question-file-list :question-number="(themeIndex + 1) + '.' + (qIndex + 1)" :question-id="question.id"></question-file-list>
              </div>
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
            <button type="submit" @click.prevent="back(1)" class="btn btn-secondary ml-auto">
              < Retour
            </button>
            <button type="submit" @click.prevent="saveDraft" class="btn btn-primary">
              <i class="fe fe-save"></i>
              Enregistrer le brouillon
            </button>
            <button type="submit" class="btn btn-secondary ml-auto">
              Suivant >
            </button>
          </div>

        </form>

      </div>
    </div>

  </div>
</template>

<script>
import Vue from 'vue'

import ConfirmModal from '../utils/ConfirmModal'
import EventBus from '../events'
import InfoBar from '../utils/InfoBar'
import QuestionFileList from '../questions/QuestionFileList'
import QuestionFileUpload from '../questions/QuestionFileUpload'
import Wizard from '../utils/Wizard'

import reportValidity from 'report-validity'

export default Vue.extend({
  data() {
    return {
      body: [
        {
          title: '',
          questions: [
            { description: '' },
          ],
        },
      ],
      errors: [],
    }
  },
  components: {
    ConfirmModal,
    InfoBar,
    QuestionFileList,
    QuestionFileUpload,
    Wizard,
  },
  mounted() {
    const loadBody = function (data) {
      console.debug('QuestionnaireBodyCreate loadBody', data)
      // Empty old themes
      this.body = []
      // Replace with new themes
      if (!data.themes) {
        return
      }
      data.themes.forEach(theme => {
        console.debug('theme', theme)
        this.body.push(theme)
      })
    }.bind(this)

    this.$parent.$on('questionnaire-updated', function(data) {
      loadBody(data)
      EventBus.$emit('question-files-changed')
    })
  },
  methods: {
    back: function(clickedStep) {
      if (!this.validateForm()) {
        return
      }
      this.$emit('back', clickedStep, this.body)
    },
    createBody: function() {
      if (!this.validateForm()) {
        return
      }
      console.debug('QuestionnaireBodyCreate createBody', this.body)
      this.$emit('body-created', this.body)
    },
    addQuestion: function(themeIndex) {
      console.debug('addQuestion', themeIndex)
      this.body[themeIndex].questions.push({ description: '' })
    },
    addTheme: function() {
      console.debug('addTheme')
      this.body.push({ title: '', questions: [{ description: '' }] })
    },
    deleteQuestion: function(themeIndex, qIndex) {
      this.body[themeIndex].questions.splice(qIndex, 1)
    },
    deleteTheme: function(themeIndex) {
      this.body.splice(themeIndex, 1)
    },
    saveDraft(event) {
      console.debug('save draft', event)
      if (!this.validateForm()) {
        return
      }
      this.$emit('save-draft', this.body)
    },
    validateForm: function() {
      const form = this.$refs.form
      return reportValidity(form)
    },
  },
})
</script>

<style>
</style>
