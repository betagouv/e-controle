<template>
<div class="row container-fluid">
  <template v-if="editMode">
    <div class="col">
      <form @submit.prevent="">
        <div class="form-group mb-6">
          <label id="title-label" class="form-label">Quel est le nom du contrôle pour lequel vous ouvrez cet espace de dépôt ?<span class="form-required">*</span></label>
          <input type="text" class="form-control" v-model="control.title" required aria-labelledby="title-label">
        </div>

        <div class="form-group">
          <label id="organization-label" class="form-label">Quel est le nom de l’organisme qui va déposer les réponses ?<span class="form-required">*</span></label>
          <input type="text" class="form-control" v-model="control.depositing_organization" required aria-labelledby="organization-label">
        </div>
        <div class="text-right">
          <a href="javascript:void(0)"
             @click="quitEditMode"
             class="btn btn-secondary">
            Annuler
          </a>
          <button type="submit"
                  @click="quitEditMode"
                  class="btn btn-primary">
            Enregistrer
          </button>
        </div>
      </form>
    </div>
  </template>
  <template v-else>
    <div class="col">
      <div v-if="control.depositing_organization">
        <div class="page-title">Organisme interrogé : {{ control.depositing_organization }}</div>
        <div class="card-title">Procédure : {{ control.title }}</div>
      </div>
      <div v-else>
        <div class="page-title mt-2">{{ control.title }}</div>
      </div>
    </div>
    <div class="col-auto mt-4 pr-0">
      <a href="javascript:void(0)"
         class="btn btn-secondary"
         title="Modifier l'espace de dépôt"
         @click="enterEditMode"
      >
        <i class="fe fe-edit"></i>
        Modifier l'espace de dépôt
      </a>
  </template>

</div>
</template>

<script>
  import axios from 'axios'
  import Vue from "vue"

  const update_control_url = "/api/control/"
  const home_url = "/accueil/"

  axios.defaults.xsrfCookieName = 'csrftoken'
  axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'

  export default Vue.extend({
    props: {
      control: Object,
    },
    data: function() {
      return {
        editMode: false,
        errorMessage: "",
        errors: "",
        hasErrors: false,
      }
    },
    methods: {
      clearErrors() {
        this.errors = ""
        this.hasErrors = false
      },
      enterEditMode() {
        this.editMode = true
      },
      quitEditMode() {
        this.editMode = false
      }
    }
  })

</script>
