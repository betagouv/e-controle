<template>
<div class="modal fade remove-user-modal" id="removeUserModal" tabindex="-1" role="dialog" aria-labelledby="removeUserModal" aria-hidden="true">
  <div class="modal-dialog modal-sm modal-notify modal-danger" role="document">
    <div class="modal-content text-center">
      <div class="modal-body">
        <div class="alert alert-warning">
          <h4>Confirmer la suppression</h4>
          <p>
            {{ editingUser.first_name }} {{ editingUser.last_name }} n'aura plus accès à ce contrôle : {{ editingControl.title }}.
          </p>
          <div class="btn-list">
            <button @click="remove()" class="btn btn-danger" type="button" data-dismiss="modal">Supprimer</button>
            <button class="btn btn-secondary" type="button" data-dismiss="modal">Annuler</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<script lang="ts">
  import { mapFields } from 'vuex-map-fields';
  import Vue from "vue";

  import { store } from '../store'
  import EventBus from '../events';

  export default Vue.extend({
    store,
    data: () {
      return {
        postResult: {}
      }
    },
    computed: {
      ...mapFields([
        'editingUser',
        'editingControl'
      ]),
    },
    methods: {
      remove() {
      var postData = { control: this.editingControl.id }
      this.axios.post('/api/user/' + this.editingUser.id + '/remove-control/', postData)
        .then(response => {
          this.postResult = response.data
          EventBus.$emit('users-changed', this.postResult);
        })
      }
    }
  })
</script>

<style></style>
