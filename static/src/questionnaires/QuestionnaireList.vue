<template>
  <div class="card">
    <div class="card-status card-status-top bg-blue"></div>
    <div class="card-header">
      <div class="card-title">
        <i class="fe fe-list mr-2"></i>
        <span>Questionnaires</span>
      </div>
    </div>

    <div class="table-responsive">
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
              <help-tooltip text="Seule la personne affectée à la rédaction du questionnaire peut le modifier."></help-tooltip>
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
                <div class="tag tag-lime round-tag font-italic">Publié</div>
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
                <small>
                  {{ questionnaire.editor.first_name }} {{ questionnaire.editor.last_name }}
                </small>
              </div>
            </td>
            <td class="w-1 text-right">
              <template v-if="!user.is_inspector">
                <a :href="questionnaire.url"
                   class="btn btn-primary"
                   title="Déposer et consulter vos réponses"
                >
                  <i class="fe fe-eye"></i>
                  Répondre
                </a>
              </template>
              <template v-else>
                <template v-if="questionnaire.is_draft">
                  <a v-if="questionnaire.editor && (user.id === questionnaire.editor.id)"
                     :href="'/questionnaire/modifier/' + questionnaire.id "
                     class="btn btn-primary"
                     title="Modifier le brouillon de questionnaire"
                  >
                    <i class="fe fe-edit"></i>
                    Modifier
                  </a>
                  <a v-else
                     :href="questionnaire.url"
                     class="btn btn-primary"
                     title="Voir le brouillon de questionnaire"
                  >
                    <i class="fe fe-eye"></i>
                    Consulter
                  </a>
                </template>
                <template v-else>
                  <a :href="questionnaire.url"
                     class="btn btn-primary"
                     title="Consulter les réponses sur E-contrôle"
                  >
                    <i class="fe fe-eye"></i>
                    Consulter
                  </a>
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
  import DateFormat from '../utils/DateFormat.js';
  import HelpTooltip from "../utils/HelpTooltip"
  import Vue from 'vue'

  export default Vue.extend({
    props: [
      'control',
      'user',
    ],
    filters: {
      DateFormat
    },
    components: {
      HelpTooltip,
    },
    computed: {
      accessibleQuestionnaires: function () {
        if (this.user.is_inspector) {
          return this.control.questionnaires
        }
        return this.control.questionnaires.filter(questionnaire => !questionnaire.is_draft)
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
</style>
