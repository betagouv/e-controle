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
      <table class="table card-table table-vcenter">
        <tbody>
          <tr v-for="questionnaire in accessibleQuestionnaires">
            <td>
              Q{{ questionnaire.numbering }}
            </td>
            <td>
                <span v-if="questionnaire.is_draft">
                  <span class="tag tag-azure round-tag font-italic">Brouillon</span>
                  <help-tooltip text="Les brouillons ne sont visibles que par l'équipe de contrôle, et sont modifiables."></help-tooltip>
                </span>
                <span>{{ questionnaire.title }}</span>
                <div v-if="questionnaire.sent_date">
                  <i class="fe fe-send"></i>
                  Date de transmission du questionnaire :
                  {{ questionnaire.sent_date }}
                </div>
                <div v-if="questionnaire.end_date">
                  <i class="fe fe-clock"></i>
                  Date de réponse souhaitée :
                  {{ questionnaire.end_date }}
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
                    Voir
                  </a>
                  <div v-if="questionnaire.editor" class="mt-1 text-nowrap">
                    <i class="fe fe-edit"></i>
                    Rédacteur : {{ questionnaire.editor.first_name }} {{ questionnaire.editor.last_name }}
                    <help-tooltip text="Seule la personne affectée à la rédaction du questionnaire peut le modifier."></help-tooltip>
                  </div>
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
  import HelpTooltip from "../utils/HelpTooltip"
  import Vue from 'vue'

  export default Vue.extend({
    props: [
      'control',
      'user',
    ],
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
