<template>

<div class="modal fade add-user-modal" id="addUserModal" tabindex="-1" role="dialog" aria-labelledby="addUserModal" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h4 class="modal-title" id="labelForModalAddUser">{{ editingControl.title }}</h4>
      </div>
      <div class="modal-body">
        <div v-if="hasErrors" class="alert alert-danger">
          L'envoi de ce formulaire n'a pas fonctionné.
        </div>
        <div v-if="editingProfileType==='inspector'" class="text-center">
            <h4><i class="fa fa-university mr-2"></i><strong>Équipe de contrôle</strong></h4>
        </div>
        <div v-if="editingProfileType==='audited'" class="text-center">
            <h4><i class="fa fa-building mr-2"></i><strong>Organisme interrogé</strong></h4>
        </div>

        <form @submit.prevent="findUser" v-if="showStep1" @keydown.esc="resetFormData">
          <fieldset class="form-fieldset">
            <div class="form-group">
              <label class="form-label">Email<span class="form-required"></span></label>
              <input type="email" class="form-control" v-bind:class="{ 'state-invalid': errors.email }" v-model="formData.email" required>
              <p class="text-muted pl-2" v-if="errors.email"><i class="fa fa-warning"></i> {{ errors.email.join(' / ')}}</p>
            </div>
          </fieldset>
          <div class="text-right">
            <button type="button" class="btn btn-secondary" @click="hideThisModal">Annuler</button>
            <button type="submit" class="btn btn-primary">Suivant</button>
          </div>
        </form>

        <form @submit.prevent="addUser" v-if="showStep2" @keydown.esc="resetFormData">
          <div class="form-fieldset">
            <p class="form-label">Email : {{ formData.email}}</p>
          </div>
          <div v-if="foundUser" class="form-fieldset">
            <p class="form-label">Prénom : {{ formData.first_name}}</p>
            <p class="form-label">Nom : {{ formData.last_name}}</p>
            <p class="form-label">Organisme : {{ formData.organization}}</p>
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
            <div class="form-group">

              <label class="form-label">Administration/Entreprise de l'agent<span class="form-required"></span></label>
              <input type="text" class="form-control" v-bind:class="{ 'state-invalid': errors.organization }" v-model="formData.organization">
              <p class="text-muted pl-2" v-if="errors.organization"><i class="fa fa-warning"></i> {{ errors.organization.join(' / ')}}</p>
            </div>
          </fieldset>
          <div class="alert alert-icon alert-primary alert-dismissible" role="alert">
            <i class="fe fe-bell mr-2" aria-hidden="true"></i>
            <button type="button" class="close" data-dismiss="alert"></button>
            <p>
              Pensez à informer la personne ajoutée qu'elle pourra désormais se connecter
              avec son email. Voici le lien à lui envoyer :
            </p>
            <p style="word-wrap: break-word;">
              https://e-controle-beta.ccomptes.fr
            </p>
          </div>
          <div class="text-right">
            <button type="button" class="btn btn-secondary" @click="hideThisModal">Annuler</button>
            <button type="submit" class="btn btn-primary">Ajouter</button>
          </div>
        </form>

      </div>
    </div>
  </div>
</div>
</template>

<script lang="ts">
  import { mapFields } from 'vuex-map-fields'
  import axios from 'axios'
  import Vue from "vue";
  import VueAxios from 'vue-axios'

  import { store } from '../store'
  import EventBus from '../events';

  Vue.use(VueAxios, axios)

  axios.defaults.xsrfCookieName = 'csrftoken'
  axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"

  export default Vue.extend({
    store,
    data: () {
      return {
        'formData': {
            'first_name': '',
            'last_name': '',
            'email': '',
            'organization': '',
            'control': '',
            'profile_type': ''
        },
        'postResult': [],
        'errors': [],
        'hasErrors': false,
        'searchResult': {},
        'foundUser': false,
        'showStep1': true,
        'showStep2': false,
      }
    },
    computed: {
      ...mapFields([
        'editingControl'
        'editingProfileType',
      ]),
    },
    methods: {
      hideThisModal() {
          this.resetFormData()
        $('#addUserModal').modal('hide');
      },
      resetFormData() {
        this.formData = {
            'first_name': '',
            'last_name': '',
            'email': '',
            'organization': '',
            'control': '',
            'profile_type': ''
        }
        this.showStep1 = true
        this.showStep2 = false
        this.foundUser = false
        this.hasErrors = false
        this.errors = []
      },
      addUser() {
        this.formData.control = this.editingControl.id
        this.formData.profile_type = this.editingProfileType
        this.axios.post('/api/user/', this.formData)
          .then(response => {
            this.postResult = response.data
            EventBus.$emit('users-changed', this.postResult)
            this.hideThisModal()
          })
          .catch((error) => {
            this.hasErrors = true
            this.errors = error.response.data
          })
      },
      findUser() {
        this.axios.get('/api/user/', {
            params: {
              search: this.formData.email
            }
          })
          .then(response => {
            this.searchResult = response.data
            if(response.data.length) {
              this.foundUser = true
              Object.assign(this.formData, response.data[0])
            }
            this.showStep1 = false
            this.showStep2 = true
          })
      }
    }
  })
</script>

<style></style>
