<template>
  <div class="modal" tabindex="-1" role="dialog" :data-keyboard="!noClose" :data-backdrop="noClose ? 'static' : true">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <slot></slot>
      </div>
    </div>
  </div>

</template>

<script>
  import Vue from "vue"

  export default Vue.extend({
    props: ['no-close'],
  })

</script>

<style></style>
