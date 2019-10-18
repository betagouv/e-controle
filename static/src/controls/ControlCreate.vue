<template>
  <div>
    <a href="javascript:void(0)"
       class="btn btn-primary"
       data-toggle="modal"
       data-target="#controlcreate">
      <i class="fe fe-plus"></i>
      Ajouter un espace de dépôt
    </a>


    <confirm-modal-with-wait id="controlcreate"
                             cancel-button="Annuler"
                             confirm-button="Créer l'espace de dépôt"
                             title="Créer un nouvel espace de dépôt"
                             @confirm="createControl"
    >
      <div>
        <info-bar>
          Chaque espace de dépôt n'est visible que par les personnes que vous inviterez.
        </info-bar>

        <form>
          <div class="form-group mb-6">
            <label class="form-label">Quel est le nom du contrôle pour lequel vous ouvrez cet espace de dépôt ?<span class="form-required">*</span></label>
            <div id="title-help" class="text-muted">
              Exemple : Contrôle des comptes et de la gestion de la Fédération Française de Football. 255 caractères maximum.
            </div>
            <input type="text" class="form-control" v-model="title" maxlength="255" required aria-describedby="title-help">
          </div>

          <div class="form-group mb-6">
            <label class="form-label">Quel est le nom de l’organisme qui va déposer les réponses ?<span class="form-required">*</span></label>
            <div id="organization-help" class="text-muted">
              Exemple : Ministère des Sports. 255 caractères maximum.
            </div>
            <input type="text" class="form-control" v-model="organization" maxlength="255" required aria-describedby="organization-help">
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
                     pattern="^[\.\s\w-]+$"
                     maxlength="255"
                     title="Ce champ ne doit pas contenir de caractères spéciaux tels que ! , @ # $ / \"
                     aria-describedby="reference-code-help">
            </div>
          </div>

        </form>
      </div>
    </confirm-modal-with-wait>
  </div>
</template>

<script>
  import axios from 'axios'
  import Vue from "vue"

  import ConfirmModalWithWait from "../utils/ConfirmModalWithWait"
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
        errorMessage: "",
        hasErrors: false,
      }
    },
    computed: {
      reference_code_prefix: function () {
        return this.year + "_"
      }
    },
    components: {
      ConfirmModalWithWait,
      ErrorBar,
      InfoBar,
    },
    methods: {
      clearErrors: function() {
        this.errorMessage = ''
        this.hasErrors = false
      },
      createControl: function(processingDoneCallback) {
        // todo validate form
        this.clearErrors()
        const payload = {
          title: this.title,
          depositing_organization: this.organization,
          reference_code: this.reference_code_prefix + this.reference_code_suffix,
        }
        axios.post(create_control_url, payload)
          .then(response => {
            console.debug(response)
            processingDoneCallback(null, response)
            // Force reload
            window.location.href = home_url + "?reload=" + Math.random() + '#control-' + response.data.id
          })
          .catch((error) => {
            console.error('Error creating control', error)

            const makeErrorMessage = (error) => {
              if (error.response && error.response.data && error.response.data['reference_code']) {
                if (error.response.data['reference_code'][0] === 'UNIQUE') {
                  return 'Le nom abrégé "' + payload.reference_code +
                      '" existe déjà pour un autre espace. Veuillez en choisir un autre.'
                }
                if (error.response.data['reference_code'][0] === 'INVALID') {
                  return 'Le nom abrégé "' + payload.reference_code +
                      '" ne doit pas contenir de caractères spéciaux tels que "! , @ # $ / \\".' +
                      ' Veuillez en choisir un autre.'
                }
              }

              if (error.message && error.message === 'Network Error') {
                return "L'espace de dépôt n'a pas pu être créé. Erreur : problème de réseau"
              }

              if (error.message) {
                return "L'espace de dépôt n'a pas pu être créé. Erreur : " + error.message
              }

              return "L'espace de dépôt n'a pas pu être créé."
            }

            this.errorMessage = makeErrorMessage(error)
            processingDoneCallback(this.errorMessage)
            this.hasErrors = true
          })
      },
      cancel: function() {
        this.clearErrors()
      },
    }
  })

</script>
