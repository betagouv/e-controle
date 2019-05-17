<template>

<div class="modal fade update-user-modal" id="updateUserModal" tabindex="-1" role="dialog" aria-labelledby="updateUserModal" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h4 class="modal-title" id="labelForModalAddUser">{{ editingControl.title }}</h4>
      </div>
      <div class="modal-body">
        <div v-if="hasErrors" class="alert alert-danger">
          L'envoi de ce formulaire n'a pas fonctionné.
        </div>

            <div class="form-group">
              <p class="form-label">Email : {{ editingUser.email}}</p>
              <p class="small text-muted">Pour modifier un email, vous devez supprimer l'utilisateur et en créer un nouveau.</p>
              <button class="btn btn-secondary btn-sm"
                      data-toggle="modal"
                      data-target="#removeUserModal"
                      @click="updateEditingState(user)">
                Supprimer l'utilisateur
              </button>
            </div>
            <hr/>
        <form @submit.prevent="updateUser">
          <fieldset class="form-fieldset">
            <div class="form-group">
              <div class="custom-controls-stacked">
                <label class="custom-control custom-radio custom-control-inline">
                  <input type="radio" v-model="editingUser.profile_type" value="inspector" class="custom-control-input" name="control-inline-radios">
                  <span class="custom-control-label">Équipe de contrôle</span>
                </label>
                <label class="custom-control custom-radio custom-control-inline">
                  <input type="radio" v-model="editingUser.profile_type" value="audited" class="custom-control-input" name="control-inline-radios">
                  <span class="custom-control-label">Organisme Contrôlé</span>
                </label>
                <p class="text-muted pl-2" v-if="errors.profile_type"><i class="fa fa-warning"></i> Choisissez l'une des options</p>
              </div>
            </div>
            <div class="form-group">
              <label class="form-label">Prénom<span class="form-required"></span></label>
              <input type="text" class="form-control" v-bind:class="{ 'state-invalid': errors.first_name }" v-model="editingUser.first_name">
              <p class="text-muted pl-2" v-if="errors.first_name"><i class="fa fa-warning"></i> {{ errors.first_name.join(' / ')}}</p>
            </div>
            <div class="form-group">
              <label class="form-label">Nom<span class="form-required"></span></label>
              <input type="text" class="form-control" v-bind:class="{ 'state-invalid': errors.last_name }" v-model="editingUser.last_name">
              <p class="text-muted pl-2" v-if="errors.last_name"><i class="fa fa-warning"></i> {{ errors.last_name.join(' / ')}}</p>
            </div>
            <div class="form-group">
              <label class="form-label">Organisme<span class="form-required"></span></label>
              <input type="text" class="form-control" v-bind:class="{ 'state-invalid': errors.organization }" v-model="editingUser.organization">
              <p class="text-muted pl-2" v-if="errors.organization"><i class="fa fa-warning"></i> {{ errors.organization.join(' / ')}}</p>
            </div>
          </fieldset>
          <div class="text-right">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">Annuler</button>
            <button type="submit" class="btn btn-primary">Modifier</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</div>
</template>

<script lang="ts">
  import { mapFields } from 'vuex-map-fields';
  import axios from 'axios'
  import Vue from "vue";
  import VueAxios from 'vue-axios'
  import Vuex from 'vuex'

  import { store } from '../store'
  import EventBus from '../events';

  Vue.use(Vuex);
  Vue.use(VueAxios, axios)

  axios.defaults.xsrfCookieName = 'csrftoken'
  axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'

  export default Vue.extend({
    store,
    data: () {
      return {
        'postResult': [],
        'errors': [],
        'hasErrors': false
      }
    },
    computed: {
      ...mapFields([
        'editingUser',
        'editingControl'
      ]),
    },
    methods: {
      hideModal() {
        $('.update-user-modal').modal('hide');
      },
      updateUser() {
        this.axios.post('/api/user/', this.editingUser)
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
      remove(user) {
        this.hideModal()
        this.editingControl = this.control
        this.editingUser = user
        this.hasErrors = false
        this.errors = {}
      }
    }
  })
</script>

<style></style>
