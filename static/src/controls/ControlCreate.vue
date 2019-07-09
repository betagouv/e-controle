<template>
  <div>
    <div class="page-header">
      <div class="page-title">
        Créer un nouvel espace de dépôt
      </div>
    </div>

    <error-bar v-if="hasErrors">
      L'envoi de ce formulaire n'a pas fonctionné. Erreur : {{JSON.stringify(errors)}}
    </error-bar>

    <info-bar>
      Vous pouvez créer un espace de dépôt pour chaque organisme interrogé dans le cadre de votre contrôle. Par exemple,
      pour le contrôle des comptes et de la gestion de l’Agence Z, vous pouvez créer deux espaces de dépôt distincts :
      un pour l’Agence Z et un autre pour le Ministère Z chargé de sa tutelle. L’Agence Z ne verra pas l’espace de dépôt
      du Ministère et inversement.
    </info-bar>

    <form @submit.prevent="showModal">
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
        <button type="submit"
                class="btn btn-primary">
          Créer l'espace de dépôt
        </button>
      </div>
    </form>

    <confirm-modal id="confirmModal"
               title="Confirmer la création d'un espace de dépôt"
               confirm-button="Oui, créer l'espace"
               cancel-button="Non, j'ai encore des modifications"
               @confirm="createControl"
    >
      <p>
        Vous êtes sur le point de confirmer la création d’un espace de dépôt pour :
      </p>
      <p>
        <em>
          {{organization}}
        </em>
      </p>
      <p>
        dans le cadre de la procédure :
      </p>
      <p>
        <em>
          {{title}}
        </em>
      </p>
      <info-bar>
        Si vous confirmez, vous pourrez créer votre premier questionnaire et ajouter les comptes d’accès des membres de
        votre équipe de contrôle.
      </info-bar>
    </confirm-modal>

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
        backUrl: home_url,
        organization: "",
        reference_code: "",
        title: "",
        errors: "",
        hasErrors: false,
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
      showModal: function() {
        $('#confirmModal').modal('show');
      },
      createControl: function() {
        this.clearErrors()

        const payload = {
          title: this.title,
          reference_code: this.reference_code,
        }
        axios.post(create_control_url, payload)
          .then(response => {
            console.debug(response)
            window.location.href = home_url + "#control-" + response.data.id
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