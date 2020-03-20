<template>
  <div class="card">
    <div class="card-status card-status-top bg-blue"></div>
    <div class="card-header">
      <div class="card-title">
        <i class="fe fe-list mr-2"></i>
        <span>Questionnaires</span>
      </div>
    </div>

    <div>
      <div v-if="accessibleQuestionnaires.length === 0"
           class="alert alert-icon alert-secondary m-2">
        <i class="fe fe-info mr-2" aria-hidden="true"></i>
        Il n'y a pas encore de questionnaire pour cet espace de dépôt.
      </div>
      <table v-else class="table card-table table-vcenter">
        <thead>
          <tr>
            <th v-if="user.is_inspector">
              Statut
              <help-tooltip text="Un questionnaire est d'abord en Brouillon : il est modifiable et l'organisme interrogé ne le voit pas. Puis il est Publié : il n'est plus modifiable et l'organisme interrogé le voit."></help-tooltip>
            </th>
            <th>Titre</th>
            <th>Date de réponse</th>
            <th v-if="user.is_inspector">
              Rédacteur
            </th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="questionnaire in accessibleQuestionnaires" :key="'questionnaire-' + questionnaire.id">
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
                <help-tooltip v-if="questionnaire.editor.id !== user.id"
                              text="Cette personne dispose des droits pour modifier ce questionnaire.
                                    Vous pourrez modifier ce questionnaire en cliquant sur 'consulter',
                                    puis 'Obtenir les droits de rédaction'"
                              icon-class="fe fe-lock">
                </help-tooltip>
                <small>
                  {{ questionnaire.editor.first_name }} {{ questionnaire.editor.last_name }}
                  <div v-if="questionnaire.modified_date" class="text-muted">
                    {{ questionnaire.modified_date }} à
                    {{  questionnaire.modified_time }}
                  </div>
                </small>
              </div>
            </td>
            <td class="w-1 action-column">
              <template v-if="!user.is_inspector">
                <div class="text-right">
                  <a :href="questionnaire.url"
                    class="btn btn-primary"
                    title="Déposer et consulter vos réponses"
                  >
                    <i class="fe fe-eye"></i>
                    Répondre
                  </a>
                </div>
              </template>
              <template v-else>
                <template v-if="questionnaire.is_draft && !!questionnaire.editor && questionnaire.editor.id === user.id">
                  <div class="text-right">
                    <div class="btn-group">
                      <a class="btn btn-primary"
                        :href="'/questionnaire/modifier/' + questionnaire.id"
                        title="Modifier le brouillon de questionnaire">
                        <i class="fe fe-edit"></i>
                        Modifier
                      </a>
                      <button type="button"
                              class="btn btn-primary dropdown-toggle dropdown-toggle-split ml-1"
                              data-toggle="dropdown"
                              aria-haspopup="true"
                              aria-expanded="false">
                        <span class="sr-only">Menu d'actions</span>
                      </button>
                      <div class="dropdown-menu dropdown-menu-right">
                        <a class="dropdown-item"
                            :href="exportUrl(questionnaire)"
                            target="_blank"
                            title="Exporter">
                          <i class="fe fe-file-text mr-2"></i>
                          Exporter
                        </a>
                        <button class="dropdown-item text-danger"
                                type="button"
                                @click="showQuestionnaireDeleteModal(questionnaire.id)">
                          <i class="fe fe-trash-2 mr-2"></i>
                          Supprimer...
                        </button>
                      </div>
                    </div>
                  </div>
                  <questionnaire-delete-modal :id="'questionnaireDeleteModal-' + questionnaire.id"
                                              :questionnaire="questionnaire">
                  </questionnaire-delete-modal>
                </template>
                <template v-else>
                  <div class="text-right">
                    <a :href="questionnaire.url"
                      class="btn btn-primary ml-2"
                      title="Voir le brouillon de questionnaire"
                    >
                      <i class="fe fe-eye"></i>
                      Consulter
                    </a>
                  </div>
                </template>
              </template>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="user.is_inspector" class="card-footer flex-row justify-content-end">
      <a :href="'/questionnaire/controle-' + control.id + '/creer'" class="btn btn-primary">
        <i class="fe fe-plus"></i>
        Ajouter un questionnaire
      </a>
    </div>

  </div>
</template>

<script>
import backendUrls from '../utils/backend'
import DateFormat from '../utils/DateFormat.js'
import HelpTooltip from '../utils/HelpTooltip'
import QuestionnaireDeleteModal from './QuestionnaireDeleteModal'
import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default Vue.extend({
  props: [
    'control',
    'user',
  ],
  filters: {
    DateFormat,
  },
  components: {
    HelpTooltip,
    QuestionnaireDeleteModal,
  },
  computed: {
    accessibleQuestionnaires: function () {
      if (this.user.is_inspector) {
        return this.control.questionnaires
      }
      return this.control.questionnaires.filter(questionnaire => !questionnaire.is_draft)
    },
  },
  methods: {
    exportUrl(questionnaire) {
      return backendUrls['questionnaire-export'](questionnaire.id)
    },
    showQuestionnaireDeleteModal(questionnaireId) {
      $('#questionnaireDeleteModal-' + questionnaireId + ' .confirm-modal').modal('show')
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
    min-width: 13em;
  }

</style>
