<template>
<div class="row container-fluid">
  <template v-if="editMode">
    <div class="col">
      <error-bar v-if="hasErrors">
        <div>
          L'espace de dépôt n'a pas pu être modifié. Erreur : {{JSON.stringify(errors)}}
        </div>
      </error-bar>
      <form @submit.prevent="updateControl" class="mb-4">
        <div class="card-title mb-4 mt-3">Modifier l'espace de dépôt</div>
        <fieldset class="form-fieldset">
          <div class="form-group">
            <label id="organization-label" class="form-label">Quel est le nom de l’organisme qui va déposer les réponses ?<span class="form-required">*</span></label>
            <input type="text" class="form-control" v-model="organization" required aria-labelledby="organization-label" maxlength="255">
          </div>
          <div class="form-group mb-6">
            <label id="title-label" class="form-label">Quel est le nom du contrôle pour lequel vous ouvrez cet espace de dépôt ?<span class="form-required">*</span></label>
            <input type="text" class="form-control" v-model="title" required aria-labelledby="title-label" maxlength="255">
          </div>
        </fieldset>
        <div class="text-right">
          <a href="javascript:void(0)"
             @click="cancel"
             class="btn btn-secondary">
            Annuler
          </a>
          <button type="submit"
                  class="btn btn-primary">
            Modifier l'espace de dépôt
          </button>
        </div>
      </form>
    </div>
  </template>
  <template v-else>
    <div class="col">
      <div v-if="organization">
        <div class="mb-3">
          <div class="text-muted font-italic">Organisme interrogé</div>
          <div class="page-title">{{ organization }}</div>
        </div>
        <div class="mb-3">
          <div class="text-muted font-italic">Procédure</div>
          <div class="card-title">{{ title }}</div>
        </div>
      </div>
      <div v-else>
        <div class="page-title mt-2">{{ title }}</div>
      </div>
    </div>
    <div class="col-auto mt-4 pr-0" v-if="sessionUser.is_inspector">
      <a href="javascript:void(0)"
         class="btn btn-secondary"
         title="Modifier l'espace de dépôt"
         @click="enterEditMode"
      >
        <i class="fe fe-edit"></i>
        Modifier
      </a>
    </div>
  </template>
</div>
</template>

<script>
  import { mapFields } from 'vuex-map-fields'
  import axios from 'axios'
  import Vue from "vue"

  import ErrorBar from "../utils/ErrorBar"

  axios.defaults.xsrfCookieName = 'csrftoken'
  axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'

  export default Vue.extend({
    props: {
      control: Object,
    },
    data: function() {
      return {
        editMode: false,
        title: "",
        organization: "",
        errors: "",
        hasErrors: false
      }
    },
    computed: {
      ...mapFields([
        'sessionUser'
      ]),
    },
    components: {
      ErrorBar
    },
    mounted() {
      this.restoreForm()
    },
    methods: {
      restoreForm() {
        this.title = this.control.title
        this.organization = this.control.depositing_organization
      },
      clearErrors() {
        this.errors = ""
        this.hasErrors = false
      },
      enterEditMode() {
        this.clearErrors()
        this.editMode = true
      },
      quitEditMode() {
        this.clearErrors()
        this.editMode = false
      },
      cancel() {
        this.restoreForm()
        this.quitEditMode()
      },
      updateControl: function() {
        const update_control_url = `/api/control/${this.control.id}/`
        const payload = {
          title: this.title,
          depositing_organization: this.organization
        }
        axios.put(update_control_url, payload)
          .then(response => {
            console.debug(response)
            this.title = response.data.title
            this.organization = response.data.depositing_organization
            this.quitEditMode()
          })
          .catch((error) => {
            console.error(error)
            this.errors = error.response.data
            this.hasErrors = true
          })
      }
    }
  })

</script>
