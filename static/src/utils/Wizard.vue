<template>
  <div class="flex-row justify-content-around mb-6">
    <wizard-step v-for="(stepTitle, i) in stepTitles"
                 :number="i+1"
                 :class="{ 'active': activeI === i , 'done': activeI > i }"
                 :clickable="activeI  === (i-1) || activeI === (i+1)"
                 @clickedStep="clicked(i+1)"
    >
      {{ stepTitle }}
    </wizard-step>
  </div>
</template>

<script>
  import Vue from 'vue'
  import WizardStep from './WizardStep'

  export default Vue.extend({
    props: [ 'active-step-number', 'step-titles' ],
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
        if (clickedStepNumber - this.activeStepNumber === 1) {
          this.$emit('next')
          return
        }
        if (clickedStepNumber - this.activeStepNumber === -1) {
          this.$emit('previous')
          return
        }
      },
    },
  })

</script>