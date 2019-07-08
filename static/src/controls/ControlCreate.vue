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
      pour le contrôle des comptes et de la gestion de l’Agence Z, vous pouvez créer deux espaces de dépôt distincts :
      un pour l’Agence Z et un autre pour le Ministère Z chargé de sa tutelle. L’Agence Z ne verra pas l’espace de dépôt
      du Ministère et inversement.
    </div>

    <form @submit.prevent="bloup">
      <fieldset class="form-fieldset">
        <div class="form-group">
          <label class="form-label">Nom de l’organisme interrogé<span class="form-required">*</span></label>
          <div id="name-help" class="text-muted">Exemple : Agence Z ou Ministère Z</div>
          <input type="text" class="form-control" v-model="organization" required aria-describedby="name-help">
        </div>
        <div class="form-group">
          <label class="form-label">Procédure de contrôle<span class="form-required">*</span></label>
          <div id="procedure-help" class="text-muted">Exemple : Contrôle des comptes et de la gestion de l’Agence Z</div>
          <input type="text" class="form-control" v-model="title" required aria-describedby="procedure-help">
        </div>
        <div class="form-group">
          <label class="form-label">Nom court de cet espace de dépôt<span class="form-required">*</span></label>
          <div id="reference-code-help" class="text-muted">
            Il s’agit du nom du dossier contenant les pièces déposées.
            Exemple : CCG_2019_AGENCEZ
          </div>
          <input type="text" class="form-control" v-model="reference_code" required aria-describedby="reference-code-help">
        </div>
      </fieldset>
      <div class="text-right">
        <a :href="backUrl" class="btn btn-secondary">
          Annuler
        </a>
        <button type="submit" @click.prevent="bloup" class="btn btn-primary">Créer l'espace de dépôt</button>
      </div>
    </form>

  </div>
</template>

<script>
  import Vue from "vue"

  export default Vue.extend({
    data: function() {
      return {
        backUrl: "/accueil/",
        organization: "",
        reference_code: "",
        title: "",
      }
    }
  })

</script>