<template>
  <div>
    <div class="card-header">
      <div class="card-title">
        Créer un nouvel espace de dépôt
      </div>
    </div>

    <div class="card-body">
      <error-bar v-if="hasErrors">
        L'envoi de ce formulaire n'a pas fonctionné. Erreur : {{JSON.stringify(errors)}}
      </error-bar>

      <form @submit.prevent="createControl">
        <div class="form-group mb-6">
          <label class="form-label">Nom de l’espace de dépôt<span class="form-required">*</span></label>
          <input type="text" class="form-control" v-model="title" required>
        </div>

        <div class="form-group mb-6">
          <label class="form-label">Nom de dossier de cet espace de dépôt<span class="form-required">*</span></label>
          <div id="reference-code-help" class="text-muted">
            Nom du dossier contenant les pièces déposées, qui apparaîtra dans votre explorateur Windows. Nous conseillons
            un nom qui soit clair pour vous pour que vous retrouviez facilement le dossier, et qui ne dépasse pas 20 caractères.
            Exemple : FFF_MinSports
          </div>
          <div class="input-group">
            <span class="input-group-prepend" id="basic-addon3">
              <span class="input-group-text">{{ reference_code_prefix }}</span>
            </span>
            <input type="text" class="form-control" v-model="reference_code_suffix" required aria-describedby="reference-code-help">
          </div>
        </div>

        <div class="text-right">
          <button type="submit"
                  class="btn btn-primary">
            Créer l'espace de dépôt
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  import Vue from "vue"

  import ConfirmModal from "../utils/ConfirmModal"
  import ErrorBar from "../utils/ErrorBar"
  import InfoBar from "../utils/InfoBar"

  const create_control_url = "/api/control/"
  const home_url = "/accueil/"

  axios.defaults.xsrfCookieName = 'csrftoken'
  axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'

  export default Vue.extend({
    data: function() {
      return {
        title: "",
        reference_code_suffix: "",
        year: new Date().getFullYear(),
        errors: "",
        hasErrors: false,
      }
    },
    computed: {
      reference_code_prefix: function () {
        return this.year + "_"
      }
    },
    components: {
      ConfirmModal,
      ErrorBar,
      InfoBar,
    },
    methods: {
      clearErrors: function() {
        this.errors = ""
        this.hasErrors = false
      },
      createControl: function() {
        this.clearErrors()
        const payload = {
          title: this.title,
          reference_code: this.reference_code_prefix + this.reference_code_suffix,
        }
        axios.post(create_control_url, payload)
          .then(response => {
            console.debug(response)
            // Force reload
            window.location.href = home_url + "?reload=" + Math.random()
          })
          .catch((error) => {
            console.error(error)
            this.errors = error.response.data
            this.hasErrors = true
          })
      },
    }
  })

</script>
