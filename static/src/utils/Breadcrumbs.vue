<template>
  <div class="flex-row">
    <div class="mx-2">
      <i class="fa fa-archive"></i>
    </div>
    <div class="mx-2">
      >
    </div>
    <div class="mx-2">
      {{ control.reference_code }} -
      {{ control.depositing_organization !== undefined ?
            control.depositing_organization : control.title}}
    </div>
  </div>
</template>

<script>
import Vue from 'vue'

export default Vue.extend({
  props: {
    control: Object,
  },
})
</script>
