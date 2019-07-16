<template>
  <div>
    <div class="wizard-step card-title">{{ number }}</div>
    <slot></slot>
  </div>
</template>

<script>
  import Vue from "vue"

  export default Vue.extend({
    props: ['number']
  })
</script>