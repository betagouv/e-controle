<template>
  <div class="sidebar">
    <div v-if="showSidebar">
      <button id="toggle-button" class="btn btn-secondary" @click="toggleCollapse">
        <i class="fe fe-sidebar"></i>
        <span v-show="collapsed">Ouvrir le menu</span>
        <span v-show="!collapsed">Fermer le menu</span>
      </button>
      <sidebar-menu class="sidebar-body"
                    :menu="menu"
                    :relative="true"
                    :hideToggle="true"
                    :show-one-child="true"
                    theme="white-theme"
                    :collapsed="collapsed"
                    widthCollapsed="0px"
      >
        <template v-slot:header>
          <div class="card-header flex-row justify-content-center border-top">
            <div class="card-title text-nowrap">
              Mes espaces de dépôt
            </div>
          </div>

          <div v-if="isLoaded && controls.length === 0">
            <div class="text-muted card-title text-center mx-7 mt-10 mb-4">
              <div v-if="user.is_inspector">
                Vous n'avez pas encore créé d'espace de dépôt.
              </div>
              <div v-else>
                Vous n'avez pas d'espace de dépôt.
              </div>
            </div>
          </div>

          <div v-if="user && user.is_inspector"
              class="card-header flex-row justify-content-center border-0">
            <control-create></control-create>
          </div>

          <div v-if="isLoaded && controls.length === 0"
              class="ie-margin-for-footer">
            <!-- empty div. Adds margin-bottom to fix a footer bug for IE. -->
          </div>

          <div v-if="!isLoaded && !hasError"
              class="sidebar-load-message card-header border-0 mt-4 mb-4">
            <div class="loader mr-2"></div>
            En attente de la liste d'espaces...
          </div>

          <error-bar id="sidebar-error-bar" v-if="hasError" noclose=true>
            <div>
              Nous n'avons pas pu obtenir vos espaces de dépôt.
            </div>
            <div class="mt-2">
              Erreur : {{ errorMessage }}
            </div>
            <div class="mt-2">
              Vous pouvez essayer de recharger la page, ou
              <a :href="'mailto:' + errorEmailLink + JSON.stringify(error)"
                target="_blank"
              >
                cliquez ici pour nous contacter
              </a>.
            </div>
          </error-bar>
        </template>
      </sidebar-menu>
    </div>
  </div>
</template>

<script>
import backend from '../utils/backend.js'
import ControlCreate from '../controls/ControlCreate'
import ErrorBar from '../utils/ErrorBar'
import { mapState } from 'vuex'
import { loadStatuses } from '../store'
import { SidebarMenu } from 'vue-sidebar-menu'
import Vue from 'vue'
import 'vue-sidebar-menu/dist/vue-sidebar-menu.css'

const ERROR_EMAIL_BODY = 'Bonjour,%0D%0A%0D%0A' +
    'Je voudrais vous signaler une erreur lors du chargement des espaces de dépôt dans le menu.' +
    ' Les détails sont ci-dessous.%0D%0A%0D%0ACordialement,%0D%0A%0D%0A%0D%0A-----------%0D%0A'
const ERROR_EMAIL_SUBJECT = 'Erreur de chargement des espaces de dépôt'
const ERROR_EMAIL_TO = 'e-controle@beta.gouv.fr'

export default Vue.extend({
  components: {
    ControlCreate,
    ErrorBar,
    SidebarMenu,
  },
  props: {
    // Pass window object as prop, so that we can pass a mock for testing.
    // Do not use "window" or "document" directly in this file, instead use "this.window" and
    // "this.window.document"
    window: {
      default: () => window,
    },
  },
  data() {
    return {
      collapsed: false,
      hasError: false,
      error: undefined,
      errorMessage: undefined,
      errorEmailLink: ERROR_EMAIL_TO + '?subject=' + ERROR_EMAIL_SUBJECT +
          '&body=' + ERROR_EMAIL_BODY,
      isMenuBuilt: false,
      menu: [],
      showSidebar: true,
    }
  },
  computed: {
    ...mapState({
      user: 'sessionUser',
      userLoadStatus: 'sessionUserLoadStatus',
      controls: 'controls',
      controlsLoadStatus: 'controlsLoadStatus',
    }),
    isLoaded() {
      return this.controlsLoadStatus === loadStatuses.SUCCESS &&
          this.userLoadStatus === loadStatuses.SUCCESS
    },
  },
  watch: {
    controlsLoadStatus(newValue, oldValue) {
      if (this.showSidebar && newValue === loadStatuses.ERROR) {
        this.displayError('Erreur lors du chargement des espaces. Essayez de recharger la page.')
        return
      }
    },
    userLoadStatus(newValue, oldValue) {
      if (this.showSidebar && newValue === loadStatuses.ERROR) {
        this.displayError('Erreur lors du chargement des espaces. Essayez de recharger la page.')
        return
      }
    },
    isLoaded(newValue, oldValue) {
      if (this.showSidebar) {
        if (newValue === false) {
          return
        }
        this.buildMenu()
      }
    },
  },
  mounted: function() {
    console.debug('this.window.location.pathname', this.window.location.pathname)
    if (this.window.location.pathname === backend.welcome()) {
      this.showSidebar = false
      return
    }
  },
  methods: {
    displayError(err) {
      this.hasError = true
      this.errorMessage = err.message ? err.message : err
      this.error = err
    },
    buildMenu() {
      console.debug('build menu')
      const makeControlTitle = control => {
        let title = control.reference_code + '\n'
        if (control.depositing_organization) {
          title += control.depositing_organization
        } else {
          title += control.title
        }
        return title
      }

      const makeQuestionnaireLink = questionnaire => {
        if (!questionnaire.is_draft) {
          return backend['questionnaire-detail'](questionnaire.id)
        }
        if (questionnaire.editor && questionnaire.editor.id === this.user.id) {
          return backend['questionnaire-edit'](questionnaire.id)
        }
        return backend['questionnaire-detail'](questionnaire.id)
      }

      // If we are on a create-questionnaire page, find the control for which the questionnaire is
      // being created.
      const controlCreatingQuestionnaire =
          backend.getIdFromViewUrl(this.window.location.pathname, 'questionnaire-create')

      // If we are on a trash page, find the control for which the trash folder is.
      const questionnaireForTrash = backend.getIdFromViewUrl(this.window.location.pathname, 'trash')

      const menu = this.controls.sort((a, b) => { return b.id - a.id })
        .map(control => {
          const controlMenu = {
            icon: 'fa fa-archive',
            href: backend['control-detail'](control.id),
            title: makeControlTitle(control),
          }

          const children = control.questionnaires.map(questionnaire => {
            if (this.user.is_inspector || !questionnaire.is_draft) {
              const questionnaireItem = {
                href: makeQuestionnaireLink(questionnaire),
                title: 'Questionnaire ' + questionnaire.numbering + ' - ' + questionnaire.title,
              }
              if (questionnaireForTrash === questionnaire.id) {
                questionnaireItem.child = [{
                  href: backend.trash(questionnaire.id),
                  title: 'Corbeille',
                }]
              }
              return questionnaireItem
            }
          }).filter(item => !!item)
          if (children.length > 0) {
            controlMenu.child = children
          }

          // Add menu item for the questionnaire being created, if there is one.
          if (controlCreatingQuestionnaire === (control.id)) {
            if (!controlMenu.child) {
              controlMenu.child = []
            }
            controlMenu.child.push({
              href: backend['questionnaire-create'](control.id),
              title: 'Q' + (controlMenu.child.length + 1),
            })
          }
          return controlMenu
        })
      this.isMenuBuilt = true
      this.menu = menu
    },
    toggleCollapse() {
      this.collapsed = !this.collapsed
    },
  },
})
</script>

<style scoped>
</style>

<style>
  #sidebar-vm {
    background-color: white;
  }
  .sidebar-body {
    min-width: 350px;
  }

  /* Place toggle button outside of the sidebar, in the navbar. */
  .sidebar {
    position: relative;
  }
  #toggle-button {
    position: absolute;
    top: -60px;
    left: 182px;
  }

  /* Don't show elements sticking out of the sidebar */
  .sidebar-body {
    overflow: hidden;
  }

  /* Add borders to items */
  .v-sidebar-menu .vsm--item {
      border-bottom-width: 1px;
      border-bottom-style: solid;
      border-bottom-color: rgba(0, 40, 100, 0.12); /* same color as tabler borders */
  }
  .v-sidebar-menu .vsm--item:first-child {
      border-top-width: 1px;
      border-top-style: solid;
      border-top-color: rgba(0, 40, 100, 0.12); /* same color as tabler borders */
  }

  /* Wrap text for titles that overflow */
  .v-sidebar-menu .vsm--title {
    white-space: pre-wrap;
    /* Text was flowing over arrows */
    margin-right: 20px;
    word-break: break-word;
  }

  /* Style icons */
  .v-sidebar-menu.vsm_white-theme .vsm--icon,
  .v-sidebar-menu.vsm_white-theme .vsm--link_level-1 .vsm--icon {
    color: #495057;
    background-color: white;
  }
  .v-sidebar-menu.vsm_white-theme .vsm--link_level-1.vsm--link_exact-active .vsm--icon,
  .v-sidebar-menu.vsm_white-theme .vsm--link_level-1.vsm--link_active .vsm--icon {
    color: #495057;
    background-color: white;
  }

  /* Fix height of items when collapsed */
  .vsm_collapsed .vsm--item {
    height: 80px;
  }

</style>
