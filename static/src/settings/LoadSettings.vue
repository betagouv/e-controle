<template>
</template>

<script>
  import { mapFields } from 'vuex-map-fields'
  import { store } from '../store'
  import Vue from "vue"


  export default Vue.extend({
    props: [
      'backendSupportTeamEmail',
    ],
    computed: {
      ...mapFields([
        'supportTeamEmail'
      ]),
    },
    created() {
      // this.supportTeamEmail = this.backendSupportTeamEmail
      console.debug("Settings: recording support team email into JS store:")
      console.debug(this.SupportTeamEmail)
    }
  })
</script>
