<template>

<div class="modal fade add-user-modal" id="addUserModal" tabindex="-1" role="dialog" aria-labelledby="addUserModal" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h4 class="modal-title" id="labelForModalAddUser">{{ editingControl.title }}</h4>
      </div>
      <div class="modal-body">
        <div v-if="hasErrors" class="alert alert-danger">
          L'ajout d'utilisateur n'a pas fonctionné.
        </div>
        <div v-if="editingProfileType==='inspector'" class="text-center">
            <h4><i class="fa fa-university mr-2"></i><strong>Équipe de contrôle</strong></h4>
        </div>
        <div v-if="editingProfileType==='audited'" class="text-center">
            <h4><i class="fa fa-building mr-2"></i><strong>Organisme interrogé</strong></h4>
        </div>

        <form @submit.prevent="validateEmail" v-if="stepShown === 1" @keydown.esc="resetFormData">
          <div class="form-fieldset">
            <div class="form-group">
              <label id="email-label" class="form-label">
                Email
                <span class="form-required"></span>
              </label>
              <input type="email"
                     autocapitalize=off
                     autocorrect=off
                     class="form-control"
                     v-bind:class="{ 'state-invalid': errors.email }"
                     v-model="formData.email"
                     required
                     aria-labelledby="email-label">
              <p class="text-muted pl-2" v-if="errors.email">
                <i class="fa fa-warning"></i>
                {{ errors.email.join(' / ')}}
              </p>
            </div>
          </div>
          <div class="text-right">
            <button type="button" class="btn btn-secondary" @click="hideThisModal">Annuler</button>
            <button type="submit" class="btn btn-primary">Suivant</button>
          </div>
        </form>

        <form @submit.prevent="findUser" v-if="stepShown === 1.5" @keydown.esc="resetFormData">
          <div class="alert alert-warning alert-icon">
            <i class="fa fa-exclamation-circle mr-2" aria-hidden="true"></i>
            <div class="mb-4">
              Vous allez ajouter <strong>{{ formData.email }}</strong> comme contrôleur.
            </div>
            <div> Cet email ne finit pas par
              <strong>@ccomptes.fr</strong>
              ou
              <strong>@crtc.ccomptes.fr</strong>
              .
            </div>
          </div>
          <div class="text-right">
            <button type="button" class="btn btn-secondary" @click="back">
              C'est une erreur, Retour
            </button>
            <button type="submit" class="btn btn-primary">
              C'est volontaire, Suivant
            </button>
          </div>
        </form>

        <form @submit.prevent="addUser" v-if="stepShown === 2" @keydown.esc="resetFormData">
          <div class="form-fieldset">
            <p class="form-label">Email : {{ formData.email}}</p>
          </div>
          <div v-if="foundUser" class="form-fieldset">
            <p class="form-label">Prénom : {{ formData.first_name}}</p>
            <p class="form-label">Nom : {{ formData.last_name}}</p>
          </div>
          <fieldset v-else class="form-fieldset">
            <div class="form-group">
              <label class="form-label">Prénom<span class="form-required"></span></label>
              <input type="text" class="form-control" v-bind:class="{ 'state-invalid': errors.first_name }" v-model="formData.first_name" required>
              <p class="text-muted pl-2" v-if="errors.first_name"><i class="fa fa-warning"></i> {{ errors.first_name.join(' / ')}}</p>
            </div>
            <div class="form-group">
              <label class="form-label">Nom<span class="form-required"></span></label>
              <input type="text" class="form-control" v-bind:class="{ 'state-invalid': errors.last_name }" v-model="formData.last_name" required>
              <p class="text-muted pl-2" v-if="errors.last_name"><i class="fa fa-warning"></i> {{ errors.last_name.join(' / ')}}</p>
            </div>
          </fieldset>
          <div class="text-right">
            <button type="button" class="btn btn-secondary" @click="hideThisModal">Annuler</button>
            <button type="submit" class="btn btn-primary">Ajouter</button>
          </div>
        </form>

        <div v-if="stepShown === 3" class="flex-column align-items-center">

          <div class="flex-row align-items-center">
            <i class="fe fe-check-circle fg-success big-icon mr-4"></i>
            <h4 class="mb-0"> Utilisateur ajouté</h4>
          </div>

          <div class="mt-5">
            Vous avez ajouté {{ this.postResult.first_name }} {{ this.postResult.last_name }}.
          </div>

          <div class="mt-5">
            Pensez à l'informer qu'elle.il pourra désormais se connecter avec son email.
          </div>

          <div class="mt-5 flex-row justify-content-end">
            <button type="button" class="btn btn-secondary" @click="hideThisModal">
              Je l'ai informé.e
            </button>
            <a class="btn btn-primary ml-2"
                :href="'mailto:' + postResult.email +
                      '?subject=Bienvenue sur e-controle' +
                      '&body=' + emailBody"
                target="_blank"
                rel="noopener noreferrer"
            >
              Créer un mail pour l'informer
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<script lang="ts">
import { mapFields } from 'vuex-map-fields'
import axios from 'axios'
import backend from '../utils/backend'
import Vue from 'vue'

import { store } from '../store'
import EventBus from '../events'

axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'

export default Vue.extend({
  store,
  data() {
    return {
      formData: {
        first_name: '',
        last_name: '',
        email: '',
        control: '',
        profile_type: '',
      },
      postResult: [],
      errors: [],
      hasErrors: false,
      searchResult: {},
      foundUser: false,
      stepShown: 1,
    }
  },
  computed: {
    ...mapFields([
      'editingControl',
      'editingProfileType',
      'config.site_url',
    ]),
    emailBody: function() {
      if (this.stepShown !== 3) {
        return ''
      }

      const newline = '%0d%0a'
      const body = 'Bonjour ' + this.postResult.first_name + ' ' + this.postResult.last_name + ',' +
        newline + newline + 'Je viens de vous ajouter au contrôle "' +
        this.editingControl.title +
        '" pour l\'organisme "' +
        this.editingControl.depositing_organization +
        '", en tant que membre de ' +
        (this.editingProfileType === 'inspector'
          ? 'l\'équipe de contrôle.'
          : 'l\'organisme contrôlé.') +
        newline + newline +
        'Pour vous connecter, rendez-vous sur le site d\'e.contrôle :' +
        newline + newline +
        this.site_url +
        newline + newline +
        'Cordialement,'

      return body
    },
  },
  methods: {
    hideThisModal() {
      this.resetFormData()
      $('#addUserModal').modal('hide')
    },
    resetFormData() {
      this.formData = {
        first_name: '',
        last_name: '',
        email: '',
        control: '',
        profile_type: '',
      }
      this.stepShown = 1
      this.foundUser = false
      this.hasErrors = false
      this.errors = []
    },
    back() {
      switch (this.stepShown) {
        case 1.5:
          this.stepShown = 1
          break
        case 2:
          this.stepShown = 1
          break
        case 3:
          this.stepShown = 2
          break
        default:
          break
      }
    },
    validateEmail() {
      const isInspectorEmail = email => {
        return email.endsWith('@ccomptes.fr') || email.endsWith('@crtc.ccomptes.fr')
      }

      if (this.editingProfileType === 'inspector' && !isInspectorEmail(this.formData.email)) {
        this.stepShown = 1.5
      } else {
        this.findUser()
      }
    },
    addUser() {
      this.formData.control = this.editingControl.id
      this.formData.profile_type = this.editingProfileType
      this.formData.email = this.formData.email.toLowerCase()
      axios.post(backend.user(), this.formData)
        .then(response => {
          this.postResult = response.data
          EventBus.$emit('users-changed', this.postResult)
          this.stepShown = 3
        })
        .catch((error) => {
          this.hasErrors = true
          this.errors = error.response.data
        })
    },
    findUser() {
      this.formData.email = this.formData.email.toLowerCase()
      axios.get(backend.user(), {
        params: {
          search: this.formData.email,
        },
      })
        .then(response => {
          this.searchResult = response.data
          if (response.data.length) {
            this.foundUser = true
            Object.assign(this.formData, response.data[0])
          }
          this.stepShown = 2
        })
    },
  },
})
</script>

<style></style>
