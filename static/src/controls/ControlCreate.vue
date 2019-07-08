<template>
  <div>
    <div class="page-header">
      <div class="page-title">
        Créer un nouvel espace de dépôt
      </div>
    </div>

    <div class="alert alert-info alert-icon alert-dismissible">
      <button type="button" class="close" data-dismiss="alert"></button>
      <i class="fe fe-info" aria-hidden="true"></i>
      Vous pouvez créer un espace de dépôt pour chaque organisme interrogé dans le cadre de votre contrôle. Par exemple,
      pour le contrôle des comptes et de la gestion de l’AGENCE Z, vous pouvez créer deux espaces de dépôt distincts :
      un pour l’AGENCE Z et un autre pour le Ministère Z chargé de sa tutelle. L’AGENCE Z ne verra pas l’espace de dépôt
      du Ministère et inversement.
    </div>
  </div>
</template>

<script>
  import Vue from "vue"

  export default Vue.extend({
    data: function() {
      return {
        coucou: "coucokkkkkku"
      }
    }
  })

</script>