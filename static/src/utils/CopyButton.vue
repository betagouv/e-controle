<template>
  <div>
    <button class="btn btn-sm btn-secondary" type="button" @click="copyLink" style="position: relative;">
      <i class="fe fe-copy"></i>
      {{ buttontext }}
    </button>

    <div v-if="confirmMessage" class="alert alert-warning alert-dismissible fade show" role="alert"
        style="position: absolute; z-index:1000;">
      {{ confirmMessage }}
      <button type="button" class="close" data-dismiss="alert" aria-label="Close" @click="dismissMessage">
      </button>
    </div>

  </div>
</template>

<script>
  import Vue from "vue"

  export default Vue.extend({
    props: [
        'tocopy',
        'buttontext',
        'confirmtext'
    ],
    data: function() {
      return {
        confirmMessage: ""
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
          msg = copyWorked ? this.confirmtext : 'La copie a échoué'
        } catch (err) {
          console.error("document.execCommand('copy') did not work.", err)
          msg = 'La copie a échoué'
        }

        console.log(msg)
        this.confirmMessage = msg

        // Remove the hidden input
        document.body.removeChild(tempInput);

      },
      dismissMessage: function() {
        this.confirmMessage = undefined
      }
    }
  })

</script>