<template>
  <div class="flex-column align-items-center">
    <div class="page-title text-large mt-xl-6 mb-2">
      Bienvenue sur e.contrôle !
    </div>
    <div class="card-title mb-xl-8">
      Quelques étapes pour bien démarrer...
    </div>
    <div id="steps" class="flex-column">
      <div class="card mx-2">
        <div class="card-status card-status-top bg-blue"></div>
        <div class="card-body flex-row align-items-center">
          <i class="fa fa-2x fa-archive text-muted mr-4 p-4 border rounded"></i>
          <div class="card-title mb-0 mr-3">
            1. Créez un espace de dépôt pour chaque organisme interrogé.
          </div>
          <control-create></control-create>
        </div>
      </div>
      <div class="card mx-2">
        <div class="card-status card-status-top bg-blue"></div>
        <div class="card-body flex-row align-items-center">
          <i class="fe fa-2x fe-list text-muted mr-4 p-4 border rounded"></i>
          <div class="card-title">
            2. Créez vos questionnaires pour chaque espace de dépôt.
          </div>
        </div>
      </div>
      <div class="card mx-2">
        <div class="card-status card-status-top bg-blue"></div>
        <div class="card-body flex-row align-items-center">
          <i class="fe fa-2x fe-users text-muted mr-4 p-4 border rounded"></i>
          <div class="card-title">
            3. Partagez l'espace de dépôt avec les membres de votre équipe et ceux de l'organisme
            interrogé.
          </div>
        </div>
      </div>
      <div class="card mx-2">
        <div class="card-status card-status-top bg-blue"></div>
        <div class="card-body flex-row align-items-center">
          <i class="fa fa-2x fa-rocket text-muted mr-4 p-4 border rounded"></i>
          <div class="card-title">
            4. Publiez le questionnaire et visualisez les réponses dans votre Explorateur Windows.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ControlCreate from './ControlCreate'
import Vue from 'vue'

export default Vue.extend({
  components: {
    ControlCreate,
  },
})
</script>

<style scoped>
  #steps {
    max-width: 670px;
  }
</style>
