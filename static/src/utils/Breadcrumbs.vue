<template>
  <h5 class="flex-row mb-5 text-muted">
    <div class="mx-2">
      <i class="fa fa-archive"></i>
    </div>
    <div class="mx-2">
      &gt;
    </div>
    <div class="mx-2">
      {{ control.reference_code }} -
      {{ control.depositing_organization !== undefined ?
            control.depositing_organization : control.title}}
    </div>
  </h5>
</template>

<script>
import Vue from 'vue'

export default Vue.extend({
  props: {
    control: Object,
  },
})
</script>
