<template>
  <div class="wizard-step">
    <div class="wizard-step-thread"></div>
    <div class="wizard-step-number card-title">{{ number }}</div>
    <slot></slot>
  </div>
</template>

<script>
  import Vue from "vue"

  export default Vue.extend({
    props: ['number']
  })
</script>