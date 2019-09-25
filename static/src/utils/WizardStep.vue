<template>
  <div class="wizard-step">
    <div class="wizard-step-thread"></div>
    <div v-if="!clickable" class="wizard-step-bubble card-title">
      <span class="number">{{ number }}</span>
      <i class="done-icon fe fe-check"></i>
    </div>
    <a v-else class="wizard-step-bubble card-title" href="javascript:void(0);" @click.prevent="$emit('clickedStep')">
      <span class="number">{{ number }}</span>
      <i class="done-icon fe fe-check"></i>
    </a>
    <slot></slot>
  </div>
</template>

<script>
  import Vue from "vue"

  export default Vue.extend({
    props: ['number', 'clickable']
  })
</script>