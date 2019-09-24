<template>
  <div class="wizard-step">
    <div class="wizard-step-thread"></div>
    <div class="wizard-step-bubble card-title">
      <span class="number">{{ number }}</span>
      <i class="done-icon fe fe-check"></i>
    </div>
    <slot></slot>
  </div>
</template>

<script>
  import Vue from "vue"

  export default Vue.extend({
    props: ['number']
  })
</script>