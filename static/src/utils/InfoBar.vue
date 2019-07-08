<template>
  <div class="alert alert-info alert-icon alert-dismissible">
    <button type="button" class="close" data-dismiss="alert"></button>
    <i class="fe fe-info" aria-hidden="true"></i>
    <slot></slot>
  </div>
</template>

<script>
  import Vue from "vue"

  export default Vue.extend({})

</script>