<template>

<div class="modal fade" id="modalAddUser" tabindex="-1" role="dialog" aria-labelledby="modalAddUser" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <form @submit.prevent="addUser">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="labelForModalAddUser">Ajouter</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true"></span>
        </button>
      </div>
      <div class="modal-body">
        <fieldset class="form-fieldset">
          <div class="form-group">
            <div class="custom-controls-stacked">
              <label class="custom-control custom-radio custom-control-inline">
                <input type="radio" v-model="formData.profile_type" value="inspector" class="custom-control-input" name="control-inline-radios">
                <span class="custom-control-label">Équipe de contrôle</span>
              </label>
              <label class="custom-control custom-radio custom-control-inline">
                <input type="radio" v-model="formData.profile_type" value="audited" class="custom-control-input" name="control-inline-radios">
                <span class="custom-control-label">Organisme Controlé</span>
              </label>
            </div>
          </div>
          <div class="form-group">
            <label class="form-label">Prénom<span class="form-required"></span></label>
            <input type="text" class="form-control" v-model="formData.first_name">
          </div>
          <div class="form-group">
            <label class="form-label">Nom<span class="form-required"></span></label>
            <input type="text" class="form-control" v-model="formData.last_name">
          </div>
          <div class="form-group">
            <label class="form-label">Email<span class="form-required"></span></label>
            <input type="email" class="form-control" v-model="formData.email">
          </div>
          <div class="form-group">
            <label class="form-label">Organisme<span class="form-required"></span></label>
            <input type="text" class="form-control" v-model="formData.organization">
          </div>
        </fieldset>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Anuler</button>
        <button type="submit" class="btn btn-primary">Ajouter</button>
      </div>
    </form>
    </div>
  </div>
</div>
</template>

<script lang="ts">
  import Vue from "vue";

  import axios from 'axios'
  import VueAxios from 'vue-axios'

  import { mapActions } from 'vuex'
  import { store } from '../store/store';

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
            'controls': [3, 4],
            'profile_type': ''
        }
        'postResult': [],
      }
    },
    methods: {
      ...mapActions(['loadData']),
      hideModal() {
        $('#modalAddUser').modal('hide');
      },
      postData() {
        this.axios.post('/api/user/', this.formData)
          .then(response => {
            console.log(response.data)
            this.postResult = response.data
          })
      },
      addUser() {
        this.postData()
        this.loadData()
        this.hideModal()
      }
    }
  });
</script>

<style></style>
