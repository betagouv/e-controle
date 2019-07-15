<template>
  <div class="card">
    <div class="card-status card-status-left bg-blue"></div>
    <div id="add-control-button-bar" class="card-header">
      <a href="javascript:void(0)"
         class="btn btn-primary"
         data-toggle="collapse"
         data-target="#controlcreate"
         @click="hideAddControlButton">
        <i class="fe fe-plus"></i>
        Ajouter un espace de dépôt
      </a>
    </div>


    <div id="controlcreate" class="collapse">
      <div class="card-header">
        <div class="card-title">
          Créer un nouvel espace de dépôt
        </div>

        <div class="card-options">
          <button type="button"
                  class="close"
                  data-toggle="collapse"
                  data-target="#controlcreate"
                  @click="cancel">
          </button>
        </div>
      </div>

      <div class="card-body">
        <error-bar v-if="hasErrors">
          L'envoi de ce formulaire n'a pas fonctionné. Erreur : {{JSON.stringify(errors)}}
        </error-bar>
        <info-bar>
          Chaque espace de dépôt n'est visible que par les personnes que vous inviterez.
        </info-bar>

        <form @submit.prevent="createControl">
          <div class="form-group mb-6">
            <label class="form-label">Quel est le nom du contrôle pour lequel vous ouvrez cet espace de dépôt ?<span class="form-required">*</span></label>
            <div id="title-help" class="text-muted">
              Exemple : Contrôle des comptes et de la gestion de la Fédération Française de Football
            </div>
            <input type="text" class="form-control" v-model="title" required aria-describedby="title-help">
          </div>

          <div class="form-group mb-6">
            <label class="form-label">Quel est le nom de l’organisme qui va déposer les réponses ?<span class="form-required">*</span></label>
            <div id="organization-help" class="text-muted">
              Exemple : Ministère des Sports
            </div>
            <input type="text" class="form-control" v-model="organization" required aria-describedby="organization-help">
          </div>

          <div class="form-group mb-6">
            <label class="form-label">Indiquez un nom abrégé pour cet espace de dépôt :<span class="form-required">*</span></label>
            <div id="reference-code-help" class="text-muted">
              Ce nom sera celui du dossier contenant les pièces déposées. Il apparaîtra dans votre explorateur Windows. Nous
              conseillons
              un nom court (max 25 caractères) et signifiant, pour que vous retrouviez facilement le dossier.
              Exemple : FFF_MinSports
            </div>
            <div class="input-group">
            <span class="input-group-prepend" id="basic-addon3">
              <span class="input-group-text">{{ reference_code_prefix }}</span>
            </span>
              <input type="text" class="form-control" v-model="reference_code_suffix" required
                     aria-describedby="reference-code-help">
            </div>
          </div>

          <div class="text-right">
            <a href="javascript:void(0)"
               data-toggle="collapse"
               data-target="#controlcreate"
               @click="cancel"
               class="btn btn-secondary">
              Annuler
            </a>
            <button type="submit"
                    class="btn btn-primary">
              Créer l'espace de dépôt
            </button>
          </div>
        </form>
      </div>
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
        organization: "",
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
        const title = "Organisme interrogé : " + this.organization + "\n Procédure : " + this.title
        const payload = {
          title: title,
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
      hideAddControlButton: function() {
        document.getElementById('add-control-button-bar').style.display = 'none';
      },
      cancel: function() {
        this.clearErrors()
        this.showAddControlButton()
      },
      showAddControlButton: function() {
        document.getElementById('add-control-button-bar').style.display = 'flex';
      },
    }
  })

</script>
