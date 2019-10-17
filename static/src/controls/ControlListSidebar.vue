<template>
  <sidebar title="Tous mes espaces">
    <sidebar-item v-for="control in controls"
                  :link="'#control-' + control.id"
                  :text="control.depositing_organization"
                  :selected="(hash === '#control-' + control.id)"
    >
    </sidebar-item>
  </sidebar>
</template>

<script>
  import Sidebar from '../utils/Sidebar'
  import SidebarItem from '../utils/SidebarItem'
  import Vue from 'vue'

  export default Vue.extend({
    props: [
      'controls', 'hash',
    ],
    components: {
      Sidebar,
      SidebarItem,
    },
  })
</script>