<template>

<div class="modal fade update-user-modal" id="updateUserModal" tabindex="-1" role="dialog" aria-labelledby="updateUserModal" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h4 class="modal-title" id="labelForModalAddUser">{{ editingControl.title }}</h4>
      </div>
      <div class="modal-body">
        <div v-if="hasErrors" class="alert alert-danger">
          La modification d'utilisateur n'a pas fonctionné.
        </div>

            <div class="form-group">
              <p class="form-label">Email : {{ editingUser.email}}</p>
              <p class="small text-muted">
                Pour modifier un email, vous devez supprimer l'utilisateur et en créer un nouveau.
              </p>
              <button class="btn btn-secondary btn-sm" @click="showRemoveModal">
                Supprimer l'utilisateur
              </button>
            </div>
        <form @submit.prevent="updateUser" @keydown.esc="resetFormData">
          <div class="form-fieldset">
            <div class="form-group">
              <label id="first-name-label" class="form-label">
                Prénom
                <span class="form-required"></span>
              </label>
              <input type="text"
                     class="form-control"
                     v-bind:class="{ 'state-invalid': errors.first_name }"
                     v-model="editingUser.first_name"
                     required
                     aria-labelledby="first-name-label">
              <p class="text-muted pl-2" v-if="errors.first_name">
                <i class="fa fa-warning"></i>
                {{ errors.first_name.join(' / ')}}
              </p>
            </div>
            <div class="form-group">
              <label id="last-name-label" class="form-label">
                Nom
                <span class="form-required"></span>
              </label>
              <input type="text"
                     class="form-control"
                     v-bind:class="{ 'state-invalid': errors.last_name }"
                     v-model="editingUser.last_name"
                     required
                     aria-labelledby="last-name-label">
              <p class="text-muted pl-2" v-if="errors.last_name">
                <i class="fa fa-warning"></i>
                {{ errors.last_name.join(' / ')}}
              </p>
            </div>
          </div>
          <div class="text-right">
            <button type="button" class="btn btn-secondary" @click="hideThisModal">Annuler</button>
            <button type="submit" class="btn btn-primary">Modifier</button>
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
import backend from '../utils/backend'
import Vue from 'vue'
import Vuex from 'vuex'

import { store } from '../store'
import EventBus from '../events'

Vue.use(Vuex)

axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'

export default Vue.extend({
  store,
  data: function() {
    return {
      postResult: [],
      errors: [],
      hasErrors: false,
    }
  },
  computed: {
    ...mapFields([
      'editingUser',
      'editingControl',
    ]),
  },
  methods: {
    showRemoveModal() {
      this.hideThisModal()
      $('#removeUserModal').modal('show')
    },
    hideThisModal() {
      this.resetFormData()
      $('#updateUserModal').modal('hide')
    },
    resetFormData() {
      this.hasErrors = false
      this.errors = []
    },
    updateUser() {
      axios.post(backend.user(), this.editingUser)
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
  },
})
</script>

<style></style>
