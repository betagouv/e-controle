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
                       v-model="themes[themeIndex].title"
                       oninvalid="this.setCustomValidity('Veuillez remplir ou supprimer les thèmes vides.')"
                       oninput="this.setCustomValidity('')"
                       :aria-describedby="'theme' + (themeIndex + 1) + 'Help'"
                       required>
                <span>
                  <a v-if="themes[themeIndex].questions.length === 0"
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
                  <a :class="{ disabled: qIndex === 0 }"
                     class="btn btn-secondary btn-sm"
                     role="button"
                     href="javascript:;"
                     @click="moveQuestionUp(themeIndex, qIndex)">
                    <i class="fa fa-chevron-up"></i>
                  </a>
                  <div class="my-1">
                    <label v-bind:for="'question' + (themeIndex + 1) + '.' + (qIndex + 1)"
                           class="mb-0">
                      <span class="stamp stamp-md bg-blue">
                        {{ themeIndex + 1 }}.{{ qIndex + 1 }}
                      </span>
                    </label>
                  </div>
                  <a :class="{ disabled: qIndex === (theme.questions.length - 1) }"
                     class="btn btn-secondary btn-sm"
                     role="button"
                     href="javascript:;"
                     @click="moveQuestionDown(themeIndex, qIndex)">
                    <i class="fa fa-chevron-down"></i>
                  </a>
                </div>
                <textarea class="form-control"
                          placeholder="Ecrivez une question ici"
                          rows="4"
                          v-bind:id="'question' + (themeIndex + 1) + '.' + (qIndex + 1)"
                          v-model="themes[themeIndex].questions[qIndex].description"
                          oninvalid="this.setCustomValidity('Veuillez remplir ou supprimer les questions vides.')"
                          oninput="this.setCustomValidity('')"
                          required>
                </textarea>

                <span>
                  <a href="javascript:void(0)"
                     @click.prevent="deleteQuestion(themeIndex, qIndex)"
                     class="btn btn-link"
                     title="Supprimer la question">
                    <i class="fe fe-trash-2"></i>
                  </a>
                </span>
                <question-file-upload :question-id="question.id"></question-file-upload>
              </div>
              <div class="card-body">
                <question-file-list :question-id="question.id">
                </question-file-list>
              </div>
            </div>

            <div class="card-footer">
              <a href="javascript:void(0)"
                 @click.prevent="addQuestion(themeIndex)"
                 class="btn btn-primary"
                 title="Ajouter une question">
                <i class="fe fe-plus"></i> Ajouter une question
              </a>
            </div>
          </div>

          <div class="card">
            <div class="card-footer">
              <div class="card-status card-status-top bg-blue">
              </div>
              <a href="javascript:void(0)"
                 @click="addTheme()"
                 class="btn btn-primary"
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

import ConfirmModal from '../utils/ConfirmModal'
import EventBus from '../events'
import InfoBar from '../utils/InfoBar'
import { mapFields } from 'vuex-map-fields'
import QuestionFileList from '../questions/QuestionFileList'
import QuestionFileUpload from '../questions/QuestionFileUpload'

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
  mounted() {
    // Todo do we still need this? Can we avoid event? Can we use store loadStatus instead?
    this.$parent.$on('questionnaire-updated', function(data) {
      EventBus.$emit('question-files-changed')
    })
  },
  methods: {
    addQuestion: function(themeIndex) {
      console.debug('addQuestion', themeIndex)
      this.themes[themeIndex].questions.push({ description: '' })
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
    // Move an element in an array from one index to the other.
    moveArrayElement(array, fromIndex, toIndex) {
      if (toIndex < 0 || toIndex > array.length - 1) {
        console.error('Cannot move the element to position', toIndex)
        return
      }
      if (fromIndex < 0 || fromIndex > array.length - 1) {
        console.error('Cannot move the element from position', fromIndex)
        return
      }
      const movingElement = array.splice(fromIndex, 1)[0]
      array.splice(toIndex, 0, movingElement)
    },
    // Run the animation for when two questions have been swapped. This should be run after the
    // state has been modified in vuex.
    animateQuestionSwap(themeIndex, fromQIndex, toQIndex) {
      if (fromQIndex === toQIndex) {
        console.error('Cannot swap question with itself! ', fromQIndex)
        return
      }

      const runAnimation = (jQuerySelector, animationClass) => {
        // Setup listener to remove the animation class once the animation is done.
        $(jQuerySelector).on(
          'animationend msAnimationEnd webkitAnimationEnd oanimationend',
          function() {
            $(this).removeClass(animationClass)
            $(this).css('z-index', 'auto')
            $(this).removeClass('bg-azure-lightest')
          },
        )
        // Add the animation class to start the animation
        $(jQuerySelector).addClass(animationClass)
      }

      if (fromQIndex > toQIndex) {
        // Selected question moves upwards
        runAnimation('#theme-' + themeIndex + '-question-' + fromQIndex, 'move-up')
        runAnimation('#theme-' + themeIndex + '-question-' + toQIndex, 'move-down')
      } else {
        // Selected question moves downwards
        runAnimation('#theme-' + themeIndex + '-question-' + toQIndex, 'move-up')
        runAnimation('#theme-' + themeIndex + '-question-' + fromQIndex, 'move-down')
      }
      // Display selected question on top during movement
      $('#theme-' + themeIndex + '-question-' + toQIndex).css('z-index', '999')
      $('#theme-' + themeIndex + '-question-' + toQIndex).addClass('bg-azure-lightest')
    },
    moveQuestionUp(themeIndex, qIndex) {
      console.debug('moveQuestionUp', themeIndex, qIndex)
      if (qIndex <= 0) {
        console.error('Cannot moveQuestionUp from index', qIndex)
        return
      }
      this.moveArrayElement(this.themes[themeIndex].questions, qIndex, qIndex - 1)
      this.animateQuestionSwap(themeIndex, qIndex, qIndex - 1)
    },
    moveQuestionDown(themeIndex, qIndex) {
      console.debug('moveQuestionDown', themeIndex, qIndex)
      if (qIndex >= (this.themes[themeIndex].questions.length - 1)) {
        console.error('Cannot moveQuestionDown from index', qIndex)
        return
      }
      this.moveArrayElement(this.themes[themeIndex].questions, qIndex, qIndex + 1)
      this.animateQuestionSwap(themeIndex, qIndex, qIndex + 1)
    },
  },
})
</script>

<style>
  @keyframes slideUp {
    from { transform : translateY(-150px) }
    to   { transform : translateY(0px) }
  }

  @keyframes slideDown {
    from { transform : translateY(150px) }
    to   { transform : translateY(0px) }
  }

  .move-up, .move-down {
    animation-duration : 1s;
    animation-iteration-count : 1;

    -webkit-animation-duration : 1s;
    -webkit-animation-iteration-count : 1;

    -moz-animation-duration : 1s;
    -moz-animation-iteration-count : 1;

    -o-animation-duration : 1s;
    -o-animation-iteration-count : 1;
  }

  .move-up {
    animation-name : slideUp;
    -webkit-animation-name : slideUp;
    -moz-animation-name : slideUp;
    -o-animation-name : slideUp;
  }

  .move-down {
    animation-name : slideDown;
    -webkit-animation-name : slideDown;
    -moz-animation-name : slideDown;
    -o-animation-name : slideDown;
  }
</style>
