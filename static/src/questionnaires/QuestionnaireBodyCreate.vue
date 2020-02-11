<template>
  <div>
    <div class="card">
      <div class="card-header">
        <div class="card-title">Etape 2 : Ajouter des questions</div>
      </div>
      <div class="card-body pb-6">
        <info-bar>
          A cette étape, vous pouvez créer votre questionnaire en ajoutant des thèmes,
          des questions et des annexes à vos questions.
        </info-bar>
        <form ref="form">
          <div class="card"
               v-for="(theme, themeIndex) in themes"
               :id="'theme-' + themeIndex"
               :key="'theme-' + themeIndex"> <!-- Card for each theme-->
            <div class="card-status card-status-top bg-blue">
            </div>

            <div class="border-bottom">
              <div class="card-header border-0">
                <div class="flex-column align-items-center mr-4">
                  <button :class="{ disabled: themeIndex === 0 }"
                          class="btn btn-secondary btn-sm move-up-button"
                          role="button"
                          type="button"
                          href="javascript:;"
                          title="Déplacer le thème vers le haut"
                          @click="moveThemeUp(themeIndex)">
                    <i class="fa fa-chevron-up"></i>
                  </button>
                  <div class="my-3">
                    <label v-bind:for="'theme' + (themeIndex + 1)" class="form-label-h3">
                      <h3 class="card-title stamp stamp-md bg-white border border-primary text-body">
                        {{themeIndex + 1}}
                      </h3>
                    </label>
                  </div>
                  <button :class="{ disabled: themeIndex === (themes.length - 1) }"
                          class="btn btn-secondary btn-sm move-down-button"
                          role="button"
                          type="button"
                          href="javascript:;"
                          title="Déplacer le thème vers le bas"
                          @click="moveThemeDown(themeIndex)">
                    <i class="fa fa-chevron-down"></i>
                  </button>
                </div>
                <div class="flex-column">
                  <div class="invisible">invisible placeholder, necessary for the layout</div>
                  <div class="flex-row">
                    <input class="form-control form-control-h3"
                          placeholder="Ecrivez un thème ici"
                          type="text"
                          maxlength="255"
                          v-bind:id="'theme' + (themeIndex + 1)"
                          v-model="themes[themeIndex].title"
                          oninvalid="this.setCustomValidity('Veuillez remplir ou supprimer les thèmes vides.')"
                          oninput="this.setCustomValidity('')"
                          :aria-describedby="'theme' + (themeIndex + 1) + 'Help'"
                          required>
                    <button v-if="themes[themeIndex].questions.length === 0"
                            @click.prevent="deleteTheme(themeIndex)"
                            role="button"
                            type="button"
                            class="btn btn-link"
                            title="Supprimer le thème"
                    >
                      <i class="fe fe-trash-2"></i>
                    </button>
                    <button v-else
                            class="btn btn-link"
                            role="button"
                            type="button"
                            data-toggle="modal"
                            :data-target="'#deleteThemeConfirmModal' + themeIndex"
                    >
                      <i class="fe fe-trash-2"></i>
                    </button>
                  </div>
                  <div class="text-muted" :id="'theme' + (themeIndex + 1) + 'Help'">
                    Exemple : "Ressources Humaines". 255 caractères maximum.
                  </div>
                </div>
              </div>
              <confirm-modal :id="'deleteThemeConfirmModal' + themeIndex"
                             title="Confirmer la suppression de ce thème"
                             confirm-button="Oui, supprimer"
                             cancel-button="Non, retour"
                             @confirm="deleteTheme(themeIndex)"
              >
                <p>
                  <span v-if="themes[themeIndex].questions.length === 1">
                    La question associée à ce thème sera également supprimée.
                  </span>
                  <span v-else>
                    Les {{ themes[themeIndex].questions.length }} questions associées à ce thème
                    seront également supprimées.
                  </span>
                </p>
              </confirm-modal>
            </div>

            <div v-for="(question, qIndex) in themes[themeIndex].questions"
                 :id="'theme-' + themeIndex + '-question-' + qIndex"
                 class="card border-0 m-0 pt-2"
                 :key="'question-' + qIndex"> <!-- Card for each question -->
              <div class="card-header border-0">
                <div class="flex-column align-items-center mr-4">
                  <button :class="{ disabled: qIndex === 0 }"
                     class="btn btn-secondary btn-sm move-up-button"
                     role="button"
                     type="button"
                     title="Déplacer la question vers le haut"
                     @click="moveQuestionUp(themeIndex, qIndex)">
                    <i class="fa fa-chevron-up"></i>
                  </button>
                  <div class="my-1">
                    <label v-bind:for="'question' + (themeIndex + 1) + '-' + (qIndex + 1)"
                           class="mb-0">
                      <span class="stamp stamp-md bg-blue">
                        {{ themeIndex + 1 }}.{{ qIndex + 1 }}
                      </span>
                    </label>
                  </div>
                  <button :class="{ disabled: qIndex === (theme.questions.length - 1) }"
                     class="btn btn-secondary btn-sm move-down-button"
                     role="button"
                     type="button"
                     title="Déplacer la question vers le bas"
                     @click="moveQuestionDown(themeIndex, qIndex)">
                    <i class="fa fa-chevron-down"></i>
                  </button>
                </div>
                <textarea class="form-control"
                          placeholder="Ecrivez une question ici"
                          rows="4"
                          v-bind:id="'question' + (themeIndex + 1) + '-' + (qIndex + 1)"
                          v-model="themes[themeIndex].questions[qIndex].description"
                          oninvalid="this.setCustomValidity('Veuillez remplir ou supprimer les questions vides.')"
                          oninput="this.setCustomValidity('')"
                          required>
                </textarea>
                <span>
                  <button @click.prevent="deleteQuestion(themeIndex, qIndex)"
                          class="btn btn-link"
                          role="button"
                          type="button"
                          title="Supprimer la question">
                    <i class="fe fe-trash-2"></i>
                  </button>
                </span>
                <question-file-upload :question="question"></question-file-upload>
              </div>
              <div class="card-body">
                <question-file-list :files="question.question_files" :with-delete="true">
                </question-file-list>
              </div>
            </div>

            <div class="card-footer">
              <button @click.prevent="addQuestion(themeIndex)"
                      class="btn btn-primary"
                      role="button"
                      type="button"
                      title="Ajouter une question">
                <i class="fe fe-plus"></i> Ajouter une question
              </button>
            </div>
          </div>

          <div class="card">
            <div class="card-footer">
              <div class="card-status card-status-top bg-blue">
              </div>
              <button @click="addTheme()"
                      class="btn btn-primary"
                      role="button"
                      type="button"
                      title="Ajouter un thème">
                <i class="fe fe-plus"></i>Ajouter un thème
              </a>
            </div>
          </div>
        </form>

      </div>
    </div>

  </div>
</template>

<script>
import Vue from 'vue'

import axios from 'axios'
import backendUrls from '../utils/backend'
import ConfirmModal from '../utils/ConfirmModal'
import InfoBar from '../utils/InfoBar'
import { mapFields } from 'vuex-map-fields'
import QuestionFileList from '../questions/QuestionFileList'
import QuestionFileUpload from '../questions/QuestionFileUpload'
import SwapAnimationMixin from './SwapAnimationMixin'

import reportValidity from 'report-validity'

export default Vue.extend({
  data() {
    return {
      errors: [],
    }
  },
  computed: {
    ...mapFields([
      'currentQuestionnaire.themes',
    ]),
  },
  components: {
    ConfirmModal,
    InfoBar,
    QuestionFileList,
    QuestionFileUpload,
  },
  mixins: [
    SwapAnimationMixin,
  ],
  methods: {
    addQuestion: function(themeIndex) {
      console.debug('addQuestion', themeIndex)
      this.themes[themeIndex].questions.push({
        description: '',
        order: this.themes[themeIndex].questions.length,
      })
    },
    addTheme: function() {
      console.debug('addTheme')
      this.themes.push({ title: '', questions: [{ description: '' }] })
    },
    deleteQuestion: function(themeIndex, qIndex) {
      this.themes[themeIndex].questions.splice(qIndex, 1)
    },
    deleteTheme: function(themeIndex) {
      this.themes.splice(themeIndex, 1)
    },
    // Used in QuestionnaireCreate.
    validateForm: function() {
      const form = this.$refs.form
      return reportValidity(form)
    },
    // For all elements in array, set the 'order' field to match with the
    // order in the array.
    // Elements are either themes or questions.
    updateOrderFields(array) {
      array.map((element, index) => {
        element.order = index
      })
    },
    moveQuestionUp(themeIndex, qIndex) {
      console.debug('moveQuestionUp, theme', themeIndex, '- question ', qIndex)
      if (qIndex <= 0) {
        console.error('Cannot moveQuestionUp from index', qIndex)
        return
      }
      this.moveArrayElement(this.themes[themeIndex].questions, qIndex, qIndex - 1)
      this.updateOrderFields(this.themes[themeIndex].questions)
      const isMoveUp = true
      this.animateSwap(
        $('#theme-' + themeIndex + '-question-' + qIndex),
        $('#theme-' + themeIndex + '-question-' + (qIndex - 1)),
        isMoveUp,
      )
    },
    moveQuestionDown(themeIndex, qIndex) {
      console.debug('moveQuestionDown, theme', themeIndex, '- question ', qIndex)
      if (qIndex >= (this.themes[themeIndex].questions.length - 1)) {
        console.error('Cannot moveQuestionDown from index', qIndex)
        return
      }
      this.moveArrayElement(this.themes[themeIndex].questions, qIndex, qIndex + 1)
      this.updateOrderFields(this.themes[themeIndex].questions)
      const isMoveUp = false
      this.animateSwap(
        $('#theme-' + themeIndex + '-question-' + qIndex),
        $('#theme-' + themeIndex + '-question-' + (qIndex + 1)),
        isMoveUp,
      )
    },
    moveThemeUp(themeIndex) {
      console.debug('themeIndex, theme', themeIndex)
      if (themeIndex <= 0) {
        console.error('Cannot moveThemeUp from index', themeIndex)
        return
      }
      this.moveArrayElement(this.themes, themeIndex, themeIndex - 1)
      this.updateOrderFields(this.themes)
      const isMoveUp = true
      this.animateSwap(
        $('#theme-' + themeIndex),
        $('#theme-' + (themeIndex - 1)),
        isMoveUp,
      )
      this.saveThemeOrder(themeIndex)
      this.saveThemeOrder(themeIndex - 1)
    },
    moveThemeDown(themeIndex) {
      console.debug('moveThemeDown, theme', themeIndex)
      if (themeIndex >= (this.themes.length - 1)) {
        console.error('Cannot moveThemeDown from index', themeIndex)
        return
      }
      this.moveArrayElement(this.themes, themeIndex, themeIndex + 1)
      this.updateOrderFields(this.themes)
      const isMoveUp = false
      this.animateSwap(
        $('#theme-' + themeIndex),
        $('#theme-' + (themeIndex + 1)),
        isMoveUp,
      )
      // Todo : should it be QuestionnaireCreate doing the backend call?
      // Todo concurrency problems : make sure the values haven't changed
      this.saveThemeOrder(themeIndex)
      this.saveThemeOrder(themeIndex + 1)
      // Todo update last saved date in UI
    },
    saveThemeOrder(themeIndex) {
      const theme = this.themes[themeIndex]
      return axios.put(
        backendUrls.theme(theme.id),
        {
          title: theme.title, // title is required, so add it even though we're not changing it
          order: theme.order,
        })
      // Todo deal with errors
    }
  },
})
</script>

<style>
@import './SwapAnimationMixin.css';
</style>
