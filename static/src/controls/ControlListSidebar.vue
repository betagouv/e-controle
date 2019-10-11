<template>
  <sidebar title="Tous mes espaces">
    <collapsible-sidebar-item v-for="control in controls"
                              :link="'#control-' + control.id"
                              :text="control.depositing_organization"
    >
      <div v-for="questionnaire in control.questionnaires">
        {{ questionnaire.title }}
      </div>
    </collapsible-sidebar-item>
  </sidebar>
</template>

<script>
  import Sidebar from '../utils/Sidebar'
  import CollapsibleSidebarItem from '../utils/CollapsibleSidebarItem'
  import Vue from 'vue'

  export default Vue.extend({
    props: [
      'controls',
    ],
    components: {
      Sidebar,
      CollapsibleSidebarItem,
    },
  })
</script>