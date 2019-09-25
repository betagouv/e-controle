<template>
  <div class="row justify-content-around mb-6">
  <wizard-step number="1"
               :class="{ 'active': active==='1', 'done': active==='2' || active==='3' }"
               :clickable="active==='2'"
               @clickedStep="clicked(1)">
    Renseigner l'introduction
  </wizard-step>
  <wizard-step number="2"
               :class="{ 'active': active==='2', 'done': active==='3' }"
               :clickable="active==='1' || active==='3'"
               @clickedStep="clicked(2)">
    Ajouter des questions
  </wizard-step>
  <wizard-step number="3" :class="{ 'active': active==='3' }"
               :clickable="active==='2'"
               @clickedStep="clicked(3)">
    Aperçu avant publication
  </wizard-step>
</div>

</template>

<script>
  import Vue from 'vue'
  import WizardStep from './WizardStep'

  export default Vue.extend({
    props: [ 'active' ],
    components: {
      WizardStep,
    },
    methods: {
      clicked: function(clickedStepNumber) {
        console.debug('clicked', clickedStepNumber)
        if (clickedStepNumber - this.active === 1) {
          this.$emit('next')
          return
        }
        if (clickedStepNumber - this.active === -1) {
          this.$emit('previous')
          return
        }
      },
    },
  })

</script>