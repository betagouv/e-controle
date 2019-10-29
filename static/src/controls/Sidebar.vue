<template>
  <div>
    <sidebar-menu :menu="menu" />
  </div>
</template>


<script>
  // todo move to better place

  import { SidebarMenu } from 'vue-sidebar-menu'
  import Vue from 'vue'
  import 'vue-sidebar-menu/dist/vue-sidebar-menu.css'

  export default Vue.extend({
    components: {
      SidebarMenu
    },
    data() {
      return {
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
    }
  })
</script>