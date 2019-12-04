<template>
  <div class="flex-row justify-content-around mb-6">
    <wizard-step v-for="(stepTitle, i) in stepTitles"
                 :key="'step-' + (i + 1)"
                 :number="i+1"
                 :class="{ 'active': activeI === i , 'done': activeI > i }"
                 :clickable="i === (activeI + 1) || i < activeI"
                 @clickedStep="clicked(i+1)"
    >
      {{ stepTitle }}
    </wizard-step>
  </div>
</template>

<script>
import Vue from 'vue'
import WizardStep from './WizardStep'

// We use the name "step-number" for the user-facing numbering : 1, 2, ..., n
// We use the name "i" for the internal numbering : 0, 1, ..., n-1
export default Vue.extend({
  props: ['active-step-number', 'step-titles'],
  components: {
    WizardStep,
  },
  computed: {
    activeI: function() {
      return this.activeStepNumber - 1
    },
  },
  methods: {
    clicked: function(clickedStepNumber) {
      if (clickedStepNumber === (this.activeStepNumber + 1)) {
        this.$emit('next', clickedStepNumber)
        return
      }
      if (clickedStepNumber < this.activeStepNumber) {
        this.$emit('previous', clickedStepNumber)
        return
      }
    },
  },
})

</script>
