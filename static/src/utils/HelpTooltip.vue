<template>
  <span>
    <a href="javascript:void(0);" data-toggle="tooltip" :title="text">
      <i class="fe fe-help-circle"></i>
    </a>

    <div class="tooltip bs-tooltip-top" role="tooltip">
      <div class="arrow"></div>
      <div class="tooltip-inner">
        {{ text }}
      </div>
    </div>
</span>

</template>

<script>
  import Vue from "vue"

  export default Vue.extend({
    props: [ 'text' ]
  })

</script>