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
                  :collapsed="collapsed"
                  @toggle-collapse="onToggleCollapse"
                  @item-click="onItemClick"
    />
  </div>
</template>


<script>
  import { SidebarMenu } from 'vue-sidebar-menu'
  import Vue from 'vue'
  import 'vue-sidebar-menu/dist/vue-sidebar-menu.css'

  export default Vue.extend({
    components: {
      SidebarMenu
    },
    data() {
      return {
        collapsed: false,

        menu: [
          {
            header: true,
            title: 'Main Navigation',
            hiddenOnCollapse: true
          },
          {
            href: '/',
            title: 'Dashboard',
            icon: 'fa fa-user'
          },
          {
            href: '#control-7',
            title: 'Charts',
            icon: 'fa fa-chart-area',
            child: [
              {
                href: '/charts/sublink',
                title: 'Sub Link'
              }
            ]
          }
        ]
      }
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