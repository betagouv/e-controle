<template>
  <div class="card">
    <div class="card-body alert alert-info" role="alert">
      <div class="mb-4">
        <h4><i class="fe fe-help-circle mr-1"></i>Un problème, une question ?</h4>
        Nous sommes là pour vous aider. N'hésitez pas à prendre contact avec l'équipe e.contrôle !
      </div>
      <a role="button"
         :href="'mailto:' + config.support_team_email"
         class="btn btn-primary"
         title="Contacter le support e.contrôle">
        <i class="fe fe-mail mr-1"></i>
        Contacter le support e.contrôle
      </a>
    </div>
  </div>
</template>

<script>
import { mapFields } from 'vuex-map-fields'
import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default Vue.extend({
  computed: {
    ...mapFields(['config']),
  },
})

</script>
