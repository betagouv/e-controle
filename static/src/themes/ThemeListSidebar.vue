<template>
  <sidebar title="Thèmes">
    <sidebar-item v-for="(theme, themeIndex) in themes"
                  :link="'#theme' + (themeIndex + 1)"
    >
      {{ (themeIndex + 1) + '. ' + theme.title }}
    </sidebar-item>
  </sidebar>
</template>

<script>
  import Sidebar from '../utils/Sidebar'
  import SidebarItem from '../utils/SidebarItem'
  import Vue from 'vue'

  export default Vue.extend({
    props: [
      'themes',
    ],
    components: {
      Sidebar,
      SidebarItem,
    },
  })
</script>