<template>
  <div class="card">
    <div class="card-status card-status-left bg-blue">
    </div>
    <div class="card-header">
      <control-title :control="control" :key="control.id"></control-title>
    </div>
    <div class="card-body"> <!--// opening: questionnaire_description_card_body  //-->
      <div class="card border-0 mb-0"> <!--// opening: list of questionnaires for control  //-->
        <div v-if="accessibleQuestionnaires.length > 0">
          <div class="card">
            <table class="table card-table table-vcenter">
              <tbody>
                  <tr v-for="questionnaire in accessibleQuestionnaires">
                    <td>
                      <h5>
                        <span v-if="questionnaire.is_draft">
                          <span class="tag tag-azure round-tag font-italic">Brouillon</span>
                          <help-tooltip text="Les brouillons ne sont visibles que par l'équipe de contrôle, et sont modifiables."></help-tooltip>
                        </span>
                        <span>{{ questionnaire.title_display }}</span>
                      </h5>
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
                    <td class="w-1">
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
                          <a v-if="user.id === questionnaire.author_id"
                             :href="'/questionnaire/modifier/' + questionnaire.id "
                             class="btn btn-primary"
                             title="Modifier le brouillon de questionnaire"
                          >
                            <i class="fe fe-edit"></i>
                            Modifier le brouillon
                          </a>
                          <a v-else
                             :href="questionnaire.url"
                             class="btn btn-primary"
                             title="Voir le brouillon"
                          >
                            <i class="fe fe-eye"></i>
                            Voir le brouillon
                          </a>
                          <div v-if="questionnaire.author_id" class="mt-1 text-nowrap">
                            <i class="fe fe-edit"></i>
                            Rédacteur : {{ questionnaire.author.first_name }} {{ questionnaire.author.last_name }}
                            <help-tooltip text="Le rédacteur du brouillon est la personne qui l'a créé, et qui peut le modifier."></help-tooltip>
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
        </div>
        <div v-else>
          <div class="alert alert-icon alert-secondary">
            <i class="fe fe-info mr-2" aria-hidden="true"></i>
            Il n'y a pas encore de questionnaire pour cet espace de dépôt.
          </div>
        </div>
        <div v-if="user.is_inspector" class="mb-2">
          <a :href="'/questionnaire/controle-' + control.id + '/creer'" class="btn btn-primary">
            <i class="fe fe-plus"></i>
            Ajouter un questionnaire
          </a>
        </div>
      </div> <!--// closing: list of questionnaires for control  //-->

      <user-section :control="control" :key="control.id"></user-section>

      <webdav-tip v-if="user.is_inspector" :webdavurl="webdavurl + '/' + control.reference_code"></webdav-tip>

    </div>  <!--// closing: questionnaire_description_card_body  //-->
  </div>

</template>

<script>
  import Vue from 'vue'

  import ControlTitle from "./ControlTitle"
  import HelpTooltip from "../utils/HelpTooltip"
  import UserSection from '../users/UserSection'
  import WebdavTip from './WebdavTip'

  export default Vue.extend({
    props: [
      'control',
      'user',
      'webdavurl',
    ],
    components: {
      ControlTitle,
      HelpTooltip,
      UserSection,
      WebdavTip,
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