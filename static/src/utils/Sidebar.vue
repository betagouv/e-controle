<template>
  <div>
    <div class="sidebar-header flex-row justify-content-between align-items-center">
      <a class="header-brand" href="/accueil">
        <img :src="'/static/img/e-controle.png'" class="header-brand-img" alt="logo" />
      </a>
      <a>
        <i class="page-title fe fe-menu"></i>
      </a>
    </div>

    <sidebar-menu class="sidebar-body"
                  :menu="menu"
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

  export default Vue.extend({
    components: {
      SidebarMenu
    },
    data() {
      return {
        collapsed: false,
        controls: [],

        menu: [
          {
            title: 'En attente de la liste de contrôles...',
            icon: 'btn-loading btn-secondary bg-white',
          },
        ]
      }
    },
    mounted: function() {
      console.debug('sidebar getting controls...')
      axios.get(controls_url).then((response) => {
        console.debug('sidebar got controls', response)
        this.controls = response.data
        this.menu = response.data.reverse().map(control => {
          return {
            icon: 'fa fa-building text-muted bg-white',
            href: ('#control-' + control.id),
            title: control.depositing_organization ? control.depositing_organization : control.title,
            child: control.questionnaires.map(questionnaire => {
              return {
                href: questionnaire_detail_url + questionnaire.id,
                title: questionnaire.title
              }
            }),
          }
        })
      }).catch(err => {
        console.error('sidebar got error when getting controls', err)
        // todo err.message err.response.status
      })
    },
    methods: {
      onToggleCollapse (collapsed) {
        console.log(collapsed)
        this.collapsed = collapsed
        if (collapsed) {
          $('.page').addClass('sidebar-collapsed')
        } else {
          $('.page').removeClass('sidebar-collapsed')
        }
      },
      onItemClick (event, item) {
        console.log('onItemClick')
        // console.log(event)
        // console.log(item)
      }
    },
  })
</script>

<style scoped>
  .sidebar-header {
    position: fixed;
    top: 0px;
    left: 0px;
    padding: 1rem;
    width: 350px;
  }

  .v-sidebar-menu.sidebar-body {
      top: 4rem;
  }

</style>

<style>
    /* Adjust the margin of the main body of the page, to fit the sidebar when collapsed or not. */
  .page {
      padding-left: 350px;
      -webkit-transition: 0.3s padding-left;
      transition: 0.3s padding-left;
  }

  .page.sidebar-collapsed {
      padding-left: 50px;
  }
</style>