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

    <div v-if="isLoading" class="sidebar-load-message card-header border-0 mt-4">
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
    />
  </div>
</template>


<script>
  import axios from "axios"
  import { SidebarMenu } from 'vue-sidebar-menu'
  import Vue from 'vue'
  import 'vue-sidebar-menu/dist/vue-sidebar-menu.css'

  const controls_url = '/api/control/'
  const questionnaire_detail_url = '/questionnaire/'
  const questionnaire_modify_url = '/questionnaire/modifier/'
  const welcome_url = '/bienvenue/'

  export default Vue.extend({
    components: {
      SidebarMenu
    },
    data() {
      return {
        collapsed: false,
        controls: [],
        currentUser: undefined,
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
          this.currentUser = response.data
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

      const makeQuestionnaireLink = questionnaire => {
        if (!questionnaire.is_draft) {
          return questionnaire_detail_url + questionnaire.id + '/'
        }
        if (questionnaire.author && questionnaire.author.id === this.currentUser.id) {
          return questionnaire_modify_url + questionnaire.id + '/'
        }
        return questionnaire_detail_url + questionnaire.id + '/'
      }

      const buildMenu = () => {
        const controlCreatingQuestionnaireId = findControlCreatingQuestionnaire()
        const menu =  this.controls.reverse().map(control => {

          const controlMenu = {
            icon: 'fa fa-building text-muted bg-white',
            href: '/accueil/#control-' + control.id,
            title: control.depositing_organization ? control.depositing_organization : control.title,
          }

          const children = control.questionnaires.map(questionnaire => {
              if (this.currentUser.is_inspector || !questionnaire.is_draft) {
                return {
                  href: makeQuestionnaireLink(questionnaire),
                  title: 'Q' + questionnaire.numbering + ' - ' + questionnaire.title
                }
              }
            }).filter(item => !!item)
          if (children.length > 0) {
            controlMenu.child = children
          }

          // Add menu item for the questionnaire being created, if there is one.
          if (controlCreatingQuestionnaireId === ('' + control.id)) {
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

      getCurrentUser().then(getControls).then(buildMenu)
    },
    methods: {
      moveBodyForCollapse () {
        const element = document.getElementById('page')
        element.classList.add('sidebar-collapsed')
      },
      moveBodyForUncollapse () {
        const element = document.getElementById('page')
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
  }
</style>

<style>
</style>