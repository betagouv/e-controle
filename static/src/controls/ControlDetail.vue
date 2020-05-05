<template>
  <div class="page-main flex-row">
    <div id="sidebar-vm" class="border-right">
      <sidebar></sidebar>
    </div>
    <div class="mt-3 mt-md-5 flex-grow-1 ml-6 ie-flex-row-child">
      <control-page>
      </control-page>
    </div>
  </div>
</template>

<script>
import ControlPage from './ControlPage'
import Sidebar from '../utils/Sidebar'
import Vue from 'vue'

export default Vue.extend({
  name: 'ControlDetail',
  components: {
    ControlPage,
    Sidebar,
  },
})
</script>
