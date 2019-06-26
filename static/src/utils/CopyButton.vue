<template>
  <div>
    <button class="btn btn-sm btn-secondary" type="button" @click="copyLink">
      <i class="fe fe-copy"></i>
      {{ buttontext }}
    </button>
  </div>
</template>

<script>
  import Vue from "vue"

  export default Vue.extend({
    props: [
        'tocopy',
        'buttontext'
    ],
    data: function() {
      return {
        tooltip: ""
      }
    },
    mounted: function() {
    },
    methods: {
      copyLink: function() {
        // Create hidden input to copy from
        const tempInput = document.createElement("input");
        tempInput.style = "position: absolute; left: -1000px; top: -1000px";
        tempInput.value = this.tocopy;
        document.body.appendChild(tempInput);
        // Select the text
        tempInput.select();

        let msg = ""
        try {
          const copyWorked = document.execCommand('copy')
          msg = copyWorked ? 'Copié' : 'La copie a échoué'
        } catch (err) {
          console.error("document.execCommand('copy') did not work.", err)
          msg = 'La copie a échoué'
        }

        console.log(msg)
        // Todo display msg

        // Remove the hidden input
        document.body.removeChild(tempInput);

      }
    }
  })

</script>