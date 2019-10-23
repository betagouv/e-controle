<template>
  <sidebar title="Tous mes espaces">
    <sidebar-item v-for="item in items"
                  :link="item.link"
                  :selected="item.selected"
    >
      <div class="sidebar-item-title">{{ item.text1 }}</div>
      <div class="sidebar-item-subtitle">{{ item.text2 }}</div>
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
            text1: control.depositing_organization,
            text2: control.title,
            selected: this.hash === '#control-' + control.id ,
          }
        })
      },
    },
  })
</script>