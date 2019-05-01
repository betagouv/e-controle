<template>

<div class="modal fade add-user-modal" id="addUserModal" tabindex="-1" role="dialog" aria-labelledby="addUserModal" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <form @submit.prevent="addUser">
    <div class="modal-content">
      <div class="modal-header">
        <h4 class="modal-title" id="labelForModalAddUser">{{ control.title }}</h4>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true"></span>
        </button>
      </div>
      <div class="modal-body">
        <div v-if="hasErrors" class="alert alert-danger">
          L'envoi de ce formulaire n'a pas fonctionné.
        </div>
        <div v-if="profileType==='inspector'" class="text-center">
            <h4><i class="fa fa-institution mr-2"></i><strong>Équipe de contrôle</strong></h4>
        </div>
        <div v-if="profileType==='audited'" class="text-center">
            <h4><i class="fe fe-user mr-2"></i><strong>Organisme controlé</strong></h3>
        </div>
        <fieldset class="form-fieldset">
          <div class="form-group">
            <label class="form-label">Prénom<span class="form-required"></span></label>
            <input type="text" class="form-control" v-bind:class="{ 'state-invalid': errors.first_name }" v-model="formData.first_name">
            <p class="text-muted pl-2" v-if="errors.first_name"><i class="fa fa-warning"></i> {{ errors.first_name.join(' / ')}}</p>
          </div>
          <div class="form-group">
            <label class="form-label">Nom<span class="form-required"></span></label>
            <input type="text" class="form-control" v-bind:class="{ 'state-invalid': errors.last_name }" v-model="formData.last_name">
            <p class="text-muted pl-2" v-if="errors.last_name"><i class="fa fa-warning"></i> {{ errors.last_name.join(' / ')}}</p>
          </div>
          <div class="form-group">
            <label class="form-label">Email<span class="form-required"></span></label>
            <input type="email" class="form-control" v-bind:class="{ 'state-invalid': errors.email }" v-model="formData.email">
            <p class="text-muted pl-2" v-if="errors.email"><i class="fa fa-warning"></i> {{ errors.email.join(' / ')}}</p>
          </div>
          <div class="form-group">
            <label class="form-label">Organisme<span class="form-required"></span></label>
            <input type="text" class="form-control" v-bind:class="{ 'state-invalid': errors.organization }" v-model="formData.organization">
            <p class="text-muted pl-2" v-if="errors.organization"><i class="fa fa-warning"></i> {{ errors.organization.join(' / ')}}</p>
          </div>
        </fieldset>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Annuler</button>
        <button type="submit" class="btn btn-primary">Ajouter</button>
      </div>
    </form>
    </div>
  </div>
</div>
</template>

<script lang="ts">
  import axios from 'axios'
  import Vue from "vue";
  import VueAxios from 'vue-axios'

  import EventBus from '../events';

  Vue.use(VueAxios, axios)

  axios.defaults.xsrfCookieName = 'csrftoken'
  axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"

  export default Vue.extend({
    // props: {
    //   control: Object
    // },
    data: () {
      return {
        'control': {},
        'profileType': '',
        'formData': {
            'first_name': '',
            'last_name': '',
            'email': '',
            'organization': '',
            'controls': [],
            'profile_type': ''
        },
        'postResult': [],
        'errors': [],
        'hasErrors': false
      }
    },
    methods: {
      hideModal() {
        $('.add-user-modal').modal('hide');
      },
      resetFormData() {
        this.formData = {
            'first_name': '',
            'last_name': '',
            'email': '',
            'organization': '',
            'controls': [],
            'profile_type': ''
        }
      },
      addUser() {
        this.formData.controls.push(this.control.id)
        this.formData.profile_type = this.profileType
        this.axios.post('/api/user/', this.formData)
          .then(response => {
            this.postResult = response.data
            EventBus.$emit('users-changed', this.postResult)
            this.resetFormData()
            this.hideModal()
          })
          .catch((error) => {
            this.hasErrors = true
            this.errors = error.response.data
          })
      }
    },
    mounted() {
      EventBus.$on('click-add-user', data => {
        this.control = data.control
        this.profileType = data.profileType
      })
    }
  })
</script>

<style></style>
