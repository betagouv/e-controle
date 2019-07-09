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
      <p>
        Vous allez créer un espace de dépôt pour votre contrôle, qui sera par la suite ouvert à l'organisme interrogé pour y déposer ses réponses.
      </p>
      <p>
        Si vous avez besoin d'interroger plusieurs organismes distincts pour un contrôle, créez un espace de dépôt pour
        chaque organisme. Chaque organisme interrogé n'aura accès qu'à son espace.
      </p>
      <p>
        Exemple : lors du contrôle de la DINSIC, vous avez besoin d'interroger la DINSIC elle-même ainsi que le bureau
        du Premier Ministre. Vous créez un espace avec "Organisme interrogé : DINSIC", puis vous recommencez pour un second espace avec
        "Organisme interrogé : Premier Ministre". L'équipe de la DINSIC n'aura pas accès à l'espace du Premier Ministre, et vice versa.
      </p>
    </info-bar>

    <form @submit.prevent="showModal">
      <fieldset class="form-fieldset">
        <div class="form-group mb-6">
          <label class="form-label">Nom de l’organisme interrogé<span class="form-required">*</span></label>
          <div id="depositing-help" class="text-muted">L'organisme qui va déposer les pièces. Exemple : Premier Ministre</div>
          <input type="text" class="form-control" v-model="depositing_organization" required aria-describedby="depositing-help">
        </div>
        <div class="row">
            <div class="col-6">
              <div class="form-group mb-6">
                <label class="form-label">Type de contrôle : <span class="form-required">*</span></label>
                <div id="control_type-help" class="text-muted">Exemple : CCG - Contrôle des Comptes et de la Gestion </div>
                <select class="form-control custom-select"
                        v-model="control_type"
                        required
                        aria-describedby="control_type-help">
                  <option value="">Type de contrôle</option>
                  <option v-for="t in control_types" :value="t.code">{{ t.code + ' - ' + t.name }}</option>
                </select>
              </div>
            </div>
            <div class="col-6">
              <div class="form-group mb-6">
                <label class="form-label">Organisme contrôlé: <span class="form-required">*</span></label>
                <div id="control_organization-help" class="text-muted">L'organisme qui est contrôlé. Exemple : DINSIC</div>
                <input type="text" class="form-control" v-model="controlled_organization" aria-describedby="control_organization-help" required>
              </div>
            </div>
          </div>
        <div class="form-group mb-6">
          <label class="form-label">Année d'ouverture du contrôle<span class="form-required">*</span></label>
          <div id="year-help" class="text-muted">Exemple : 2019</div>
          <select class="form-control custom-select"
                  v-model="year"
                  required
                  aria-describedby="year-help"
                  style="width: 5em;">
            <option value="">Année d'ouverture du contrôle</option>
            <option v-for="y in 30" :value="y + 2015">{{ y + 2015 }}</option>
          </select>
        </div>
        <div class="form-group mb-6">
          <label class="form-label">Nom court de cet espace de dépôt</label>
          <div id="reference-code-help" class="text-muted">
            Il s’agit du nom du dossier contenant les pièces déposées. Il est généré automatiquement en fonction de vos
            réponses aux questions ci-dessus.
          </div>
          <div>{{ reference_code }}</div>
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
          {{depositing_organization}}
        </em>
      </p>
      <p>
        dans le cadre de la procédure :
      </p>
      <p>
        <em>
          {{control_type}} - {{ controlled_organization }}
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
        control_type: "CCG",
        controlled_organization: "",
        depositing_organization: "",
        year: 2019,
        errors: "",
        hasErrors: false,
        control_types: [
          { code: "CCG", name: "Contrôle des Comptes et de la Gestion" },
          { code: "CAB", name: "Contrôle des Actes Budgétaires" },
          { code: "JUG-PROG", name: "Jugement suite à contrôle programmé par la juridiction" },
          { code: "JUG-ACP", name: "Jugement suite à arrêté de charge provisoire" },
          { code: "EQ", name: "Enquête" },
          { code: "", name: "Autre" }
        ]
      }
    },
    computed: {
      reference_code: function () {
        let out = this.year
        if (this.control_type) {
          out += "_" + this.control_type
        }
        out += "_" + this.controlled_organization
        out += "_" + this.depositing_organization.replace(/\s+/g, '')
        return out
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