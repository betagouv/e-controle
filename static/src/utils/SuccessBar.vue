<template>
  <div class="alert alert-success alert-icon alert-dismissible">
    <button v-if="!noclose" type="button" class="close" data-dismiss="alert"></button>
    <i class="fe fe-info" aria-hidden="true"></i>
    <slot></slot>
  </div>
</template>

<script>
  import Vue from "vue"

  export default Vue.extend({
    props: ['noclose']
  })

</script>
