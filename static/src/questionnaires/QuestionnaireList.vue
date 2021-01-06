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
                <div class="text-right">
                  <a
                    :href="questionnaireDetailUrl(questionnaire.id)"
                    class="btn btn-primary"
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
                    <a class="btn btn-primary"
                      :href="questionnaireEditUrl(questionnaire.id)"
                      title="Modifier le brouillon de questionnaire">
                      <i class="fe fe-edit"></i>
                      Modifier
                    </a>
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
      this.$refs['questionnaireDeleteFlow' + questionnaireId][0].start()
    },
    exportUrl(questionnaire) {
      return backendUrls['questionnaire-export'](questionnaire.id)
    },
    showModal(qId) {
      this.questionnaireId = qId
      $(this.$refs.modal.$el).modal('show')
    },
    cloneQuestionnaire() {
      const getCreateMethod = () => axios.post.bind(this, backendUrls.questionnaire())
      const curCtrl = this.controls.find(ctrl => ctrl.id === this.control.id)

      const curQuestionnaire = curCtrl.questionnaires.filter(q => q.id === this.questionnaireId)

      if (this.checkedCtrls.length) {
        const destCtrls = this.controls.filter(ctrl => this.checkedCtrls.includes(ctrl.id))
        destCtrls.map(ctrl => {
          curQuestionnaire[0] = { ...curQuestionnaire[0], control: ctrl.id, is_draft: true, id: null }
          getCreateMethod()(curQuestionnaire[0])
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
