<template>
  <sidebar>
    <template v-slot:title>
      <i class="fa fa-archive mr-2"></i>
      Tous mes espaces
    </template>
    <sidebar-item v-for="item in items"
                  :link="item.link"
                  :selected="item.selected"
    >
      <div v-if="item.organization" class="sidebar-item-title">
        <i class="fa fa-building mr-2"></i>
        {{ item.organization }}
      </div>
      <div class="sidebar-item-subtitle">
        <i class="fa fa-exchange-alt mr-2"></i>
        {{ item.procedure }}
      </div>
    </sidebar-item>
    <div class="card-header flex-row justify-content-center">
      <control-create v-if="user.is_inspector"></control-create>
    </div>
  </sidebar>
</template>

<script>
  import ControlCreate from "./ControlCreate"
  import Sidebar from '../utils/Sidebar'
  import SidebarItem from '../utils/SidebarItem'
  import Vue from 'vue'

  export default Vue.extend({
    props: [
      'controls', 'hash', 'user',
    ],
    components: {
      ControlCreate,
      Sidebar,
      SidebarItem,
    },
    computed: {
      items : function() {
        return this.controls.map(control => {
          return {
            link: '#control-' + control.id,
            organization: control.depositing_organization,
            procedure: control.title,
            selected: this.hash === '#control-' + control.id ,
          }
        })
      },
    },
  })
</script>