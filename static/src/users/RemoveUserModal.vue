<template>
<div class="modal fade remove-user-modal" id="removeUserModal" tabindex="-1" role="dialog" aria-labelledby="removeUserModal" aria-hidden="true">
  <div class="modal-dialog modal-sm modal-notify modal-danger" role="document">
    <div class="modal-content text-center">
      <div class="modal-body">
        <div class="alert alert-warning">
          <h4>Confirmer la suppression</h4>
          <p>
            {{ user.first_name }} {{ user.last_name }} n'aura plus accès à ce contrôle : {{ control.title }}.
          </p>
          <div class="btn-list">
            <button @click="remove()" class="btn btn-danger" type="button" data-dismiss="modal">Supprimer</button>
            <button class="btn btn-secondary" type="button" data-dismiss="modal">Anuler</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<script lang="ts">
  import Vue from "vue";

  import EventBus from '../events';

  export default Vue.extend({
    data: () {
      return {
        user: Object,
        control: Object,
        postResult: {}
      }
    },
    methods: {
          remove() {
          var postData = { control: this.control.id }
          this.axios.post('/api/user/' + this.user.id + '/remove-control/', postData)
            .then(response => {
              this.postResult = response.data
              EventBus.$emit('users-changed', this.postResult);
            })
        }
    },
    mounted() {
      EventBus.$on('click-remove-user', data => {
        this.control = data.control
        this.user = data.user
      })
    }
  })
</script>

<style></style>
