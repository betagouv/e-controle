<template>

<div class="modal fade update-user-modal" id="updateUserModal" tabindex="-1" role="dialog" aria-labelledby="updateUserModal" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <form @submit.prevent="updateUser">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="labelForModalAddUser">Modifier</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true"></span>
        </button>
      </div>
      <div class="modal-body">
        <div v-if="hasErrors" class="alert alert-danger">
          L'envoi de ce formulaire n'a pas fonctionné.
        </div>
        <fieldset class="form-fieldset">
          <div class="form-group">
            <div class="custom-controls-stacked">
              <label class="custom-control custom-radio custom-control-inline">
                <input type="radio" v-model="formData.profile_type" value="inspector" class="custom-control-input" name="control-inline-radios">
                <span class="custom-control-label">Équipe de contrôle</span>
              </label>
              <label class="custom-control custom-radio custom-control-inline">
                <input type="radio" v-model="formData.profile_type" value="audited" class="custom-control-input" name="control-inline-radios">
                <span class="custom-control-label">Organisme Contrôlé</span>
              </label>
              <p class="text-muted pl-2" v-if="errors.profile_type"><i class="fa fa-warning"></i> Choisissez l'une des options</p>
            </div>
          </div>
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
        <button type="submit" class="btn btn-primary">Modifier</button>
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
    data: () {
      return {
        'control': Object,
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
        $('.update-user-modal').modal('hide');
      },
      updateUser() {
        this.formData.controls.push(this.control.id)
        this.axios.post('/api/user/', this.formData)
          .then(response => {
            this.postResult = response.data
            EventBus.$emit('users-changed', this.postResult)
            this.hideModal()
          })
          .catch((error) => {
            this.hasErrors = true
            this.errors = error.response.data
          })
      },
    }
    mounted () {
        EventBus.$on('click-update-user', data => {
          this.control = data.control
          this.formData.first_name = data.user.first_name
          this.formData.last_name = data.user.last_name
          this.formData.email = data.user.email
          this.formData.controls = data.user.controls
          this.formData.profile_type = data.user.profile_type
        })
    }
  })
</script>

<style></style>
