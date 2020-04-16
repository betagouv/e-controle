<template>
  <h5 class="flex-row mb-5 text-muted">
    <div class="mx-2">
      <i class="fa fa-archive"></i>
    </div>
    <div class="mx-2">
      <i class="fa fa-chevron-right"></i>
    </div>
    <div class="mx-2">
      <a :href="controlLink">
        {{ control.reference_code }} -
        {{ control.depositing_organization !== undefined ?
              control.depositing_organization : control.title}}
      </a>
    </div>
  </h5>
</template>

<script>
/*
  Note : there are also breadcrumbs in trash.html, that don't use this component (because it's not a
  Vue page). If you change this component, maybe you will want to make the same changes to
  trash.html.
*/

import backendUrls from './backend'
import Vue from 'vue'

export default Vue.extend({
  props: {
    control: Object,
  },
  computed: {
    controlLink() {
      return backendUrls['control-detail'](this.control.id)
    },
  },
})
</script>
