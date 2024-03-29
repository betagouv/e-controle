<template>
  <div class="card">
    <confirm-modal
      ref="modal"
      cancel-button="Annuler"
      confirm-button="Dupliquer le questionnaire"
      title="Dupliquer un questionnaire"
      @confirm="cloneQuestionnaire"
    >
      <info-bar>
        Veuillez sélectionner les espaces de dépôt vers lesquels vous souhaitez dupliquer ce questionnaire.
      </info-bar>
      <form>
        <div class="form-group mb-6">
          <label v-for="ctrl in accessibleControls"
                :key="ctrl.id"
                class="custom-control custom-checkbox">
            <input type="checkbox" class="custom-control-input" :value="ctrl.id" v-model="checkedCtrls">
            <span class="custom-control-label">{{ ctrl.depositing_organization }} - {{ ctrl.title }} ({{ ctrl.reference_code }})</span>
          </label>
        </div>
      </form>
    </confirm-modal>
    <div class="card-status card-status-top bg-blue"></div>
    <div class="card-header">
      <div class="card-title">
        <i class="fe fe-list mr-2"></i>
        <span>Questionnaires</span>
      </div>
    </div>

    <div>
      <div
        v-if="accessibleQuestionnaires.length === 0"
        class="alert alert-icon alert-secondary m-2"
      >
        <i class="fe fe-info mr-2" aria-hidden="true"></i>
        Il n'y a pas encore de questionnaire pour cet espace de dépôt.
      </div>
      <table v-else class="table card-table table-vcenter">
        <thead>
          <tr>
            <th v-if="user.is_inspector">
              Statut
              <help-tooltip
                text="Un questionnaire est d'abord en Brouillon : il est modifiable et
                                  l'organisme interrogé ne le voit pas. Puis il est Publié : il
                                  n'est plus modifiable et l'organisme interrogé le voit."
              >
              </help-tooltip>
            </th>
            <th>Titre</th>
            <th>Date de réponse</th>
            <th v-if="user.is_inspector">Rédacteur</th>
            <td class="border-bottom"></td>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="questionnaire in accessibleQuestionnaires"
            :key="'questionnaire-' + questionnaire.id"
          >
            <td class="tag-column" v-if="user.is_inspector">
              <div v-if="questionnaire.is_draft">
                <div class="tag tag-azure round-tag font-italic">Brouillon</div>
              </div>
              <div v-else-if="questionnaire_has_replies(questionnaire.id) && !questionnaire_is_replied(questionnaire.id)">
                <div class="tag tag-yellow round-tag font-italic">En cours</div>
              </div>
              <div v-else-if="questionnaire_is_replied(questionnaire.id) && !questionnaire_is_finalized(questionnaire.id)">
                <div class="tag tag-orange round-tag font-italic">Répondu</div>
              </div>
              <div v-else-if="questionnaire_is_finalized(questionnaire.id)">
                <div class="tag tag-purple round-tag font-italic">Finalisé</div>
              </div>
              <div v-else>
                <div class="tag tag-green round-tag font-italic">Publié</div>
              </div>
            </td>
            <td>
              <div>Questionnaire {{ questionnaire.numbering }}</div>
              <div>{{ questionnaire.title }}</div>
            </td>
            <td class="end-date-column">
              <div v-if="questionnaire.end_date">
                <small>
                  {{ questionnaire.end_date | DateFormat }}
                </small>
              </div>
            </td>
            <td v-if="user.is_inspector" class="editor-column">
              <div v-if="questionnaire.is_draft && questionnaire.editor">
                <help-tooltip
                  v-if="questionnaire.editor.id !== user.id"
                  text="Cette personne dispose des droits pour modifier ce
                                    questionnaire. Vous pourrez modifier ce questionnaire en
                                    cliquant sur 'Consulter', puis 'Obtenir les droits de
                                    rédaction'."
                  icon-class="fe fe-lock"
                >
                </help-tooltip>
                <small>
                  {{ questionnaire.editor.first_name }}
                  {{ questionnaire.editor.last_name }}
                  <div v-if="questionnaire.modified_date" class="text-muted">
                    {{ questionnaire.modified_date }} à
                    {{ questionnaire.modified_time }}
                  </div>
                </small>
              </div>
            </td>
            <td class="w-1 action-column">
              <template v-if="!user.is_inspector">
                <div v-if="questionnaire_has_replies(questionnaire.id)" class="text-right">
                   <div class="btn-group">
                      <a class="btn btn-secondary"
                        :href="questionnaireDetailUrl(questionnaire.id)"
                        title="Déposer et consulter vos réponses">
                        <i class="fe fe-eye"></i>
                        Répondre
                      </a>
                       <button
                      type="button"
                      class="btn btn-secondary dropdown-toggle dropdown-toggle-split"
                      data-toggle="dropdown"
                      aria-haspopup="true"
                      aria-expanded="false"
                    >
                      <span class="sr-only">Menu d'actions</span>
                    </button>
                    <div class="dropdown-menu dropdown-menu-right">
                      <button
                        class="dropdown-item text-success"
                        type="button"
                        @click="markQuestionnaireAsReplied(questionnaire.id)"
                      >
                        <i class="fe fe-check"></i>
                        Marquer comme répondu
                      </button>
                    </div>
                  </div>
                </div>
                <div v-else class="text-right">
                  <a
                    :href="questionnaireDetailUrl(questionnaire.id)"
                    class="btn btn-primary ml-2"
                    title="Déposer et consulter vos réponses"
                  >
                    <i class="fe fe-eye"></i>
                    Répondre
                  </a>
                </div>
              </template>
              <template v-else>
                <template
                  v-if="
                    questionnaire.is_draft &&
                    !!questionnaire.editor &&
                    questionnaire.editor.id === user.id
                  "
                >
                  <div class="text-right">
                    <div class="btn-group">
                      <a class="btn btn-secondary"
                        :href="questionnaireEditUrl(questionnaire.id)"
                        title="Modifier le brouillon de questionnaire">
                        <i class="fe fe-edit"></i>
                        Modifier
                      </a>
                       <button
                      type="button"
                      class="btn btn-secondary dropdown-toggle dropdown-toggle-split"
                      data-toggle="dropdown"
                      aria-haspopup="true"
                      aria-expanded="false"
                    >
                      <span class="sr-only">Menu d'actions</span>
                    </button>
                    <div class="dropdown-menu dropdown-menu-right">
                      <button
                        class="dropdown-item text-danger"
                        type="button"
                        @click="startQuestionnaireDeleteFlow(questionnaire.id)"
                      >
                        <i class="fe fe-trash-2"></i>
                        Supprimer
                      </button>
                    </div>
                  </div>
                </template>
                <template v-else-if="questionnaire.is_draft &&
                                    questionnaire.editor.id !== user.id"
                >
                  <div class="text-right">
                    <a :href="questionnaireDetailUrl(questionnaire.id)"
                      class="btn btn-primary ml-2"
                      title="Voir le brouillon de questionnaire"
                    >
                      <i class="fe fe-eye"></i>
                      Consulter
                    </a>
                  </div>
                </template>
                <template v-else>
                  <div class="text-right">
                    <div class="btn-group">
                    <a
                      :href="questionnaireDetailUrl(questionnaire.id)"
                      title="Voir le questionnaire publié"
                      class="btn btn-secondary"
                    >
                      <i class="fe fe-eye"></i>
                      Consulter
                    </a>
                    <button
                      type="button"
                      class="btn btn-secondary dropdown-toggle dropdown-toggle-split"
                      data-toggle="dropdown"
                      aria-haspopup="true"
                      aria-expanded="false"
                    >
                      <span class="sr-only">Menu d'actions</span>
                    </button>
                    <div class="dropdown-menu dropdown-menu-right">
                      <button
                        class="dropdown-item"
                        type="button"
                        @click="showModal(questionnaire.id)"
                      >
                        <i class="fe fe-copy"></i>
                        Dupliquer
                      </button>
                      <button
                        v-if="questionnaire_is_replied(questionnaire.id)"
                        class="dropdown-item text-success"
                        type="button"
                        @click="markQuestionnaireAsFinalized(questionnaire.id)"
                      >
                        <i class="fe fe-check"></i>
                        Marquer comme finalisé
                      </button>
                    </div>
                  </div>
                </template>
              </template>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div
      v-if="user.is_inspector"
      class="card-footer flex-row justify-content-end"
    >
      <a :href="questionnaireCreateUrl" class="btn btn-primary">
        <i class="fe fe-plus"></i>
        Ajouter un questionnaire
      </a>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import backendUrls from '../utils/backend'
import DateFormat from '../utils/DateFormat.js'
import HelpTooltip from '../utils/HelpTooltip'
import InfoBar from '../utils/InfoBar'
import ConfirmModal from '../utils/ConfirmModal'
import Vue from 'vue'
import Vuex, { mapState } from 'vuex'

Vue.use(Vuex)

export default Vue.extend({
  props: ['control', 'user'],
  filters: {
    DateFormat,
  },
  components: {
    HelpTooltip,
    InfoBar,
    ConfirmModal,
  },
  data: function() {
    return {
      questionnaireId: null,
      checkedCtrls: [],
    }
  },
  computed: {
    ...mapState({
      controls: 'controls',
    }),
    accessibleControls() {
      return this.controls
    },
    accessibleQuestionnaires() {
      if (this.user.is_inspector) {
        return this.control.questionnaires
      }
      return this.control.questionnaires.filter(
        (questionnaire) => !questionnaire.is_draft,
      )
    },
    questionnaireCreateUrl() {
      return backendUrls['questionnaire-create'](this.control.id)
    },
  },
  methods: {
    questionnaireDetailUrl(questionnaireId) {
      return backendUrls['questionnaire-detail'](questionnaireId)
    },
    questionnaireEditUrl(questionnaireId) {
      return backendUrls['questionnaire-edit'](questionnaireId)
    },
    startQuestionnaireDeleteFlow(questionnaireId) {
      const getUpdateMethod = (qId) => axios.put.bind(this, backendUrls.questionnaire(qId))
      const curQ = this.control.questionnaires.find(q => q.id === questionnaireId)
      const newQ = { ...curQ, control: null }

      getUpdateMethod(questionnaireId)(newQ).then(response => {
        console.log(response.data)
      })
    },
    exportUrl(questionnaire) {
      return backendUrls['questionnaire-export'](questionnaire.id)
    },
    showModal(qId) {
      this.questionnaireId = qId
      $(this.$refs.modal.$el).modal('show')
    },
    questionnaire_is_replied(qId) {
      const q = this.control.questionnaires.find(q => q.id === qId)
      return q.is_replied
    },
    questionnaire_is_finalized(qId) {
      const q = this.control.questionnaires.find(q => q.id === qId)
      return q.is_finalized
    },
    questionnaire_has_replies(qId) {
      const q = this.control.questionnaires.find(q => q.id === qId)
      let found_replies = false

      if(q.themes) {
        q.themes.map(theme => {
          theme.questions.map(question => {
            if(question.response_files.length) {
              found_replies = true
            }
          })
        })
      }

      return found_replies
    },
    markQuestionnaireAsReplied(qId) {
      const getUpdateMethod = (qId) => axios.put.bind(this, backendUrls.questionnaire(qId))
      const curQ = this.control.questionnaires.find(q => q.id === qId)
      const newQ = { ...curQ, is_replied: true }

      getUpdateMethod(qId)(newQ)
    },
    markQuestionnaireAsFinalized(qId) {
      const getUpdateMethod = (qId) => axios.put.bind(this, backendUrls.questionnaire(qId))
      const curQ = this.control.questionnaires.find(q => q.id === qId)
      const newQ = { ...curQ, is_finalized: true }

      getUpdateMethod(qId)(newQ)
    },
    cloneQuestionnaire() {
      const getCreateMethod = () => axios.post.bind(this, backendUrls.questionnaire())
      const getUpdateMethod = (qId) => axios.put.bind(this, backendUrls.questionnaire(qId))

      if (this.checkedCtrls.length) {
        const curQ = this.control.questionnaires.find(q => q.id === this.questionnaireId)
        const destCtrls = this.controls.filter(ctrl => this.checkedCtrls.includes(ctrl.id))

        destCtrls.map(ctrl => {
          const themes = curQ.themes.map(t => {
            const qq = t.questions.map(q => {
              return { description: q.description }
            })
            return { title: t.title, questions: qq }
          })

          let newQ = { ...curQ, control: ctrl.id, is_draft: true, id: null, themes: [] }
          getCreateMethod()(newQ).then(response => {
            const qId = response.data.id
            newQ = { ...newQ, themes: themes }

            getUpdateMethod(qId)(newQ).then(response => {
              const updatedQ = response.data

              curQ.themes.map(t => {
                t.questions.map(q => {
                  const qId = updatedQ.themes.find(updatedT => updatedT.order === t.order)
                    .questions.find(updatedQ => updatedQ.order === q.order).id

                  q.question_files.map(qf => {
                    axios.get(qf.url, { responseType: 'blob' }).then(response => {
                      const formData = new FormData()
                      formData.append('file', response.data, qf.basename)
                      formData.append('question', qId)

                      axios.post(backendUrls.annexe(), formData, {
                        headers: {
                          'Content-Type': 'multipart/form-data',
                        },
                      })
                    })
                  })
                })
              })
            })
          })
        })
      }
    },
  },
})
</script>

<style scoped>
.tag-column {
  max-width: 7em;
}

.editor-column {
  min-width: 9em;
}

.end-date-column {
  min-width: 9em;
}

.action-column {
  min-width: 10em;
}
</style>
