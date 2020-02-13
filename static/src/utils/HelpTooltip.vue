<template>
  <span>
    <a href="javascript:void(0);" data-toggle="tooltip" data-placement="right" :title="text" class="help-tooltip">
      <i :class="iconClass"></i>
    </a>
  </span>
</template>

<script>
import Vue from 'vue'

export default Vue.extend({
  props: {
    text: String,
    iconClass: {
      type: String,
      default: 'fe fe-help-circle',
    },
  },
  mounted: function() {
    // Initialize tooltips
    $('[data-toggle="tooltip"]').tooltip()
  },
})

</script>

<style scoped>
  .help-tooltip {
    color:var(--primary);
    text-decoration: none;
  }
</style>
