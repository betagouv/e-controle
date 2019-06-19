<template>
  <span>
    <a href="javascript:void(0);" data-toggle="tooltip" :title="text" style="color:#467fcf">
      <i class="fe fe-help-circle"></i>
    </a>
  </span>
</template>

<script>
  import Vue from "vue"

  export default Vue.extend({
    props: [ 'text' ]
  })

</script>