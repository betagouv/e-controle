<template>
  <div class="sidebar">
    <div class="sidebar-header bg-white flex-row justify-content-between align-items-center">
      <a class="header-brand" href="/accueil">
        <img :src="'/static/img/e-controle.png'" class="header-brand-img" alt="logo" />
      </a>
    </div>

    <div class="card-header flex-row justify-content-center border-top">
      <div class="card-title">
        Mes espaces de dépôt
      </div>
    </div>

    <div v-if="!isLoading && controls.length === 0">
      <div class="text-muted card-title text-center mx-7 mt-10 mb-4">
        <div v-if="user.is_inspector">
          Vous n'avez pas encore créé d'espace de dépôt.
        </div>
        <div v-else>
          Vous n'avez pas d'espace de dépôt.
        </div>
      </div>
    </div>

    <div v-if="user && user.is_inspector" class="card-header flex-row justify-content-center border-0">
      <control-create></control-create>
    </div>

    <div v-if="!collapsed && isLoading" class="sidebar-load-message card-header border-0 mt-4 mb-4">
      <div class="loader mr-2"></div>
      En attente de la liste de contrôles...
    </div>

    <error-bar v-if="hasError" noclose=true>
      <div>
        Nous n'avons pas pu obtenir vos espaces de dépôt.
      </div>
      <div class="mt-2">
        Erreur : {{ errorMessage }}
      </div>
      <div class="mt-2">
        Vous pouvez essayer de recharger la page, ou
        <a :href="'mailto:' + errorEmailTo + '?subject=' + errorEmailSubject + '&body=' + errorEmailBody + JSON.stringify(error)"
           target="_blank"
        >
          cliquez ici pour nous contacter
        </a>.
      </div>
    </error-bar>

    <sidebar-menu class="sidebar-body"
                  :menu="menu"
                  :relative="true"
                  :hideToggle="true"
                  :show-one-child="true"
                  theme="white-theme"
                  :collapsed="collapsed"
                  @toggle-collapse="onToggleCollapse"
                  @item-click="onItemClick"
    >
    </sidebar-menu>

  </div>
</template>


<script>
  import axios from "axios"
  import backend from '../utils/backend.js'
  import ControlCreate from '../controls/ControlCreate'
  import ErrorBar from '../utils/ErrorBar'
  import { Vuex, mapState } from 'vuex'
  import { SidebarMenu } from 'vue-sidebar-menu'
  import Vue from 'vue'
  import 'vue-sidebar-menu/dist/vue-sidebar-menu.css'

  const error_email_body = 'Bonjour,%0D%0A%0D%0AJe voudrais vous signaler une erreur lors du chargement des espaces de dépôt dans le menu. Les détails sont ci-dessous.%0D%0A%0D%0ACordialement,%0D%0A%0D%0A%0D%0A-----------%0D%0A'
  const error_email_subject = 'Erreur de chargement des espaces de dépôt'
  const error_email_to = 'e-controle@beta.gouv.fr'

  export default Vue.extend({
    components: {
      ControlCreate,
      ErrorBar,
      SidebarMenu,
    },
    data() {
      return {
        collapsed: false,
        controls: [],
        hasError: false,
        error: undefined,
        errorMessage: '',
        errorEmailBody: error_email_body,
        errorEmailSubject: error_email_subject,
        errorEmailTo: error_email_to,
        isLoading: true,
        menu: [],
      }
    },
    computed: {
      ...mapState({
        user: 'sessionUser',
      }),
    },
    mounted: function() {
      if (window.location.pathname === backend.welcome()) {
        this.collapsed = true
        this.menu = []
        this.moveBodyForCollapse()
        // Hack for top bar to stay on top, until we figure out the layout for collapsed menu.
        const topBar = document.getElementsByClassName('sidebar-header')[0];
        topBar.setAttribute('style', 'width: 100%;')
        return
      }

      const getControls = () => {
        console.debug('sidebar getting controls...')
        return axios.get(backend.control()).then((response) => {
          console.debug('sidebar got controls', response)
          this.controls = response.data
        }).catch(err => {
          console.error('sidebar got error when getting controls', err)
          throw err
        })
      }

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

      const buildMenu = () => {
        // If we are on a create-questionnaire page, find the control for which the questionnaire is being created.
        const controlCreatingQuestionnaire = backend.getIdFromViewUrl(window.location.pathname, 'questionnaire-create')
        // If we are on a trash page, find the control for which the trash folder is.
        const questionnaireForTrash = backend.getIdFromViewUrl(window.location.pathname, 'trash')
        const menu =  this.controls.sort((a, b) => { return b.id - a.id })
            .map(control => {

          const controlMenu = {
            icon: 'fa fa-archive',
            href: backend['control-detail'](control.id),
            title: makeControlTitle(control),
          }

          const children = control.questionnaires.map(questionnaire => {
              if (this.user.is_inspector || !questionnaire.is_draft) {
                const questionnaireItem =  {
                  href: makeQuestionnaireLink(questionnaire),
                  title: 'Questionnaire ' + questionnaire.numbering + ' - ' + questionnaire.title
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
        this.isLoading = false
        this.menu = menu
      }

      const displayError = (err) => {
        this.isLoading = false
        this.hasError = true
        this.errorMessage = err.message ? err.message : err
        this.error = err
      }

      this.$store.dispatch('setSessionUser')
          .then(getControls)
          .then(buildMenu)
          .catch(displayError)
    },
    methods: {
      moveBodyForCollapse () {
        const element = document.getElementById('page-main')
        element.classList.add('sidebar-collapsed')
      },
      moveBodyForUncollapse () {
        const element = document.getElementById('page-main')
        element.classList.remove('sidebar-collapsed')
      },
      onToggleCollapse (collapsed) {
        console.log(collapsed)
        this.collapsed = collapsed
        if (collapsed) {
          this.moveBodyForCollapse()
        } else {
          this.moveBodyForUncollapse()
        }
      },
      onItemClick (event, item) {
        console.debug('onItemClick', event, item)
      }
    },
  })
</script>

<style scoped>
  .sidebar-header {
    padding: 1rem;
    width: 351px; /* 1px wider so that the right-border is hidden */
    margin-top: 1px;
  }

  .sidebar {
    width: 350px;
  }
</style>

<style>
  #sidebar-vm {
    background-color: white;
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
  .v-sidebar-menu.vsm_white-theme .vsm--link_level-1.vsm--link_exact-active .vsm--icon, .v-sidebar-menu.vsm_white-theme .vsm--link_level-1.vsm--link_active .vsm--icon {
    color: #495057;
    background-color: white;
  }

</style>