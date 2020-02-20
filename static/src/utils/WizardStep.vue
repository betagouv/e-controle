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
  </div>
</template>

<script>
import Vue from 'vue'

export default Vue.extend({
  props: ['number', 'clickable'],
})
</script>

<style scoped>
.wizard-step {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.wizard-step-graphics {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.wizard-step-thread {
    background-color: #dbdde0;
    height: 0.3em;
    width: 100%;
    position: relative;
    top: 1.2em;
    z-index: -1
}

.wizard-step-bubble {
    background-color: #dbdde0;
    color: #495057;
    border-radius: 50%;
    height: 2rem;
    width: 2rem;
    padding-top: 0.3rem;
    text-align: center;
    margin-bottom: 0.2rem;
}

.wizard-step-bubble .done-icon {
    display: none;
    margin-top: 0.2rem
}

/* Highlight clickable step on hover */
.wizard-step a:hover {
    text-decoration-line: none;
}
.wizard-step a:hover .wizard-step-bubble, .wizard-step a:hover .wizard-step-thread {
    background-color: #45aaf2;
    color: white;
}

/* Active step */
.active .wizard-step-thread {
    background-color: #45aaf2;
    color: #fff;
}
.active .wizard-step-bubble {
    background-color: #45aaf2;
    color: #fff;
}

/* Done step */
.done .wizard-step-thread, .done .wizard-step-bubble {
    background-color: #5eba00;
    color: #fff;
}
.done .wizard-step-bubble .number {
    display: none;
}
.done .wizard-step-bubble .done-icon {
    display: block;
}
</style>
