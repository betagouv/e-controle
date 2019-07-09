<template>
  <div class="alert alert-danger alert-icon alert-dismissible">
    <button type="button" class="close" data-dismiss="alert"></button>
    <i class="fe fe-alert-triangle" aria-hidden="true"></i>
    <slot></slot>
  </div>
</template>

<script>
  import Vue from "vue"

  export default Vue.extend({})

</script>