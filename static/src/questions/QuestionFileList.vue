<template>
  <div v-if="files && files.length" class="question-box-child">
    <div v-if="files.length > 1" class="form-label">Fichiers annexes à la question:</div>
    <div v-else class="form-label">Fichier annexe à la question:</div>
    <ul>
      <li v-for="(file, index) in files" :key="index">
        <a :href="file.url">{{ file.basename }}</a>
          <span>
            <a href="javascript:void(0)"
               @click.prevent="deleteFile(file.id)"
               class="btn btn-link"
               title="Supprimer le fichier">
              <i class="fe fe-trash-2"></i>
            </a>
          </span>
      </li>
    </ul>
  </div>
</template>

<script>
import EventBus from '../events'
import { mapFields } from 'vuex-map-fields'
import Vue from 'vue'

export default Vue.extend({
  props: {
    questionId: Number,
  },
  computed: {
    ...mapFields([
      'currentQuestionnaire.themes',
    ]),
    files: function() {
      const findQuestion = (themes, questionId) => {
        let out
        themes.some(theme => {
          if (!theme.questions) {
            return false
          }
          const foundQuestion = theme.questions.find(question => {
            return question.id === questionId
          })
          if (foundQuestion !== undefined) {
            out = foundQuestion
            return true
          }
          return false
        })
        return out
      }
      const foundQuestion = findQuestion(this.themes, this.questionId)
      if (foundQuestion === undefined) {
        return []
      }
      return foundQuestion.question_files
    },
  },
  methods: {
    deleteFile(fileId) {
      this.axios.delete('/api/annexe/' + fileId)
        .then(function() {
          EventBus.$emit('question-files-changed')
        })
        .catch(function(error) {
          console.log('Error when deleting question file', error)
          EventBus.$emit('display-error', 'Le fichier n\'a pu être supprimé.')
        })
    },
  },
})
</script>
