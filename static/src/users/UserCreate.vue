<template>

<div class="modal fade" id="modalAddUser" tabindex="-1" role="dialog" aria-labelledby="modalAddUser" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="exampleModalLabel">Ajouter et inviter</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true"></span>
        </button>
      </div>
      <div class="modal-body">
        <form v-on:submit="submitEntry" action="#" method="post">
        <fieldset class="form-fieldset">
          <div class="form-group">
            <div class="custom-controls-stacked">
              <label class="custom-control custom-radio custom-control-inline">
                <input type="radio" class="custom-control-input" name="example-inline-radios" value="option1" checked="">
                <span class="custom-control-label">Équipe de contrôle</span>
              </label>
              <label class="custom-control custom-radio custom-control-inline">
                <input type="radio" class="custom-control-input" name="example-inline-radios" value="option2">
                <span class="custom-control-label">Organisme Controlé</span>
              </label>
            </div>
          </div>
          <div class="form-group">
            <label class="form-label">Prénom<span class="form-required"></span></label>
            <input type="text" class="form-control" v-model="first_name">
          </div>
          <div class="form-group">
            <label class="form-label">Nom<span class="form-required"></span></label>
            <input type="text" class="form-control">
          </div>
          <div class="form-group">
            <label class="form-label">Email<span class="form-required"></span></label>
            <input type="email" class="form-control">
          </div>
          <div class="form-group">
            <label class="form-label">Organisme<span class="form-required"></span></label>
            <input type="text" class="form-control">
          </div>
        </fieldset>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Anuler</button>
        <button type="submit" class="btn btn-primary" data-dismiss="modal">Ajouter</button>
      </div>
    </div>
  </div>
</div>
</template>

<script lang="ts">
  import Vue from "vue";

  import axios from 'axios'
  import VueAxios from 'vue-axios'

  Vue.use(VueAxios, axios)

  export default Vue.extend({
    data: () {
      return {
        first_name: '',
        last_name: '',
        email: '',
        oragnization: '',
        controls: [],
        postResult: []
      }
    },
    methods: {
      submitEntry() {
        this.axios.post('/api/user/', this.data)
          .then(response => {
            this.postResult = response.data
          })
      }
    }
  });
</script>

<style></style>
