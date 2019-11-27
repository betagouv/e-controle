<template>
  <div>
    <div class="sidebar-header bg-white flex-row justify-content-between align-items-center">
      <a class="header-brand" href="/accueil">
        <img :src="'/static/img/e-controle.png'" class="header-brand-img" alt="logo" />
      </a>
      <!-- remove for now, collapse by user not supported a>
        <i class="page-title fe fe-menu"></i>
      </a-->
    </div>

    <div class="card-header flex-row justify-content-center border-top">
      <div class="card-title">
        Mes espaces de dépôt
      </div>
    </div>

    <div v-if="!isLoading && controls.length === 0">
      <div class="text-muted card-title text-center mx-7 mt-9 mb-4">
        Vous n'avez pas encore créé d'espace de dépôt.
      </div>
    </div>

    <div class="card-header flex-row justify-content-center">
      <control-create></control-create>
    </div>

    <div v-if="!collapsed && isLoading" class="sidebar-load-message card-header border-0 mt-4 mb-4">
      <div class="loader mr-2"></div>
      En attente de la liste de contrôles...
    </div>

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
  import ControlCreate from '../controls/ControlCreate'
  import { SidebarMenu } from 'vue-sidebar-menu'
  import Vue from 'vue'
  import 'vue-sidebar-menu/dist/vue-sidebar-menu.css'

  const controls_url = '/api/control/'
  const questionnaire_detail_url = '/questionnaire/'
  const questionnaire_modify_url = '/questionnaire/modifier/'
  const welcome_url = '/bienvenue/'

  export default Vue.extend({
    components: {
      ControlCreate,
      SidebarMenu,
    },
    data() {
      return {
        collapsed: false,
        controls: [],
        user: undefined,
        menu: [],
        isLoading: true,
      }
    },
    mounted: function() {
      if (window.location.pathname === welcome_url) {
        this.collapsed = true
        this.menu = []
        this.moveBodyForCollapse()
        // Hack for top bar to stay on top, until we figure out the layout for collapsed menu.
        const topBar = document.getElementsByClassName('sidebar-header')[0];
        topBar.setAttribute('style', 'width: 100%;')
        return
      }

      const getCurrentUser = () => {
        console.debug('sidebar getting current user...')
        return axios.get('/api/user/current/').then((response) => {
          console.debug('sidebar got user', response)
          this.user = response.data
        }).catch(err => {
          // todo deal with error
        })
      }

      const getControls = () => {
        console.debug('sidebar getting controls...')
        return axios.get(controls_url).then((response) => {
          console.debug('sidebar got controls', response)
          this.controls = response.data
        }).catch(err => {
          console.error('sidebar got error when getting controls', err)
          // todo err.message err.response.status
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
          return questionnaire_detail_url + questionnaire.id + '/'
        }
        if (questionnaire.editor && questionnaire.editor.id === this.user.id) {
          return questionnaire_modify_url + questionnaire.id + '/'
        }
        return questionnaire_detail_url + questionnaire.id + '/'
      }

      const buildMenu = () => {
        const controlCreatingQuestionnaireId = findControlCreatingQuestionnaire()
        const questionnaireForTrash = findQuestionnaireForTrash()
        const menu =  this.controls.sort((a, b) => { return b.id - a.id })
            .map(control => {

          const controlMenu = {
            icon: 'fa fa-archive',
            href: '/accueil/#control-' + control.id,
            title: makeControlTitle(control),
          }

          const children = control.questionnaires.map(questionnaire => {
              if (this.user.is_inspector || !questionnaire.is_draft) {
                const questionnaireItem =  {
                  href: makeQuestionnaireLink(questionnaire),
                  title: 'Questionnaire ' + questionnaire.numbering + ' - ' + questionnaire.title
                }
                if (questionnaireForTrash === '' + questionnaire.id) {
                  questionnaireItem.child = [{
                    href: '/questionnaire/corbeille/' + questionnaire.id + '/',
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
          if (controlCreatingQuestionnaireId === ('' + control.id)) {
            if (!controlMenu.child) {
              controlMenu.child = []
            }
            controlMenu.child.push({
              href: '/questionnaire/controle-' + control.id + '/creer',
              title: 'Q' + (controlMenu.child.length + 1),
            })
          }
          return controlMenu

        })
        this.isLoading = false
        this.menu = menu
      }

      // If we are on a create-questionnaire page, find the control for which the questionnaire is being created.
      const findControlCreatingQuestionnaire = () => {
        const found = window.location.pathname.match(/^\/questionnaire\/controle-([0-9]+)\/creer$/)
        if (found) {
          return found[1]
        }
      }

      // If we are on a trash page, find the control for which the trash folder is.
      const findQuestionnaireForTrash = () => {
        const found = window.location.pathname.match(/^\/questionnaire\/corbeille\/([0-9]+)\/$/)
        if (found) {
          return found[1]
        }
      }

      getCurrentUser().then(getControls).then(buildMenu)
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
    width: 350px;
    margin-top: 1px;
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
  .v-sidebar-menu .vsm--item:last-child {
      border-bottom-style: none;
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