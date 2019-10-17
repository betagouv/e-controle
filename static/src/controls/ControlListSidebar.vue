<template>
  <sidebar title="Tous mes espaces">
    <sidebar-item v-for="item in items"
                  :link="item.link"
                  :text="item.text"
                  :selected="item.selected"
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
    computed: {
      items : function() {
        console.log('items map', this.controls)
        return this.controls.map(control => {
          return {
            link: '#control-' + control.id,
            text: control.depositing_organization + ' / ' + control.title,
            selected: this.hash === '#control-' + control.id ,
          }
        })
      },
    },
  })
</script>