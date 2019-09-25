<template>
  <div class="wizard-step">

    <a v-if="clickable"
       class="wizard-step-graphics"
       href="javascript:void(0);"
       @click.prevent="$emit('clickedStep')">
      <div class="wizard-step-thread"></div>
      <div class="wizard-step-bubble card-title">
        <span class="number">{{ number }}</span>
        <i class="done-icon fe fe-check"></i>
      </div>
    </a>

    <div v-else
         class="wizard-step-graphics">
      <div class="wizard-step-thread"></div>
      <div class="wizard-step-bubble card-title">
        <span class="number">{{ number }}</span>
        <i class="done-icon fe fe-check"></i>
      </div>
    </div>

    <slot></slot>
</template>

<script>
  import Vue from "vue"

  export default Vue.extend({
    props: ['number', 'clickable']
  })
</script>