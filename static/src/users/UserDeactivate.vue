<template>
<div class="modal fade modal-deactivate-user" :id="modalId()" tabindex="-1" role="dialog" :aria-labelledby="modalId()" aria-hidden="true">
  <div class="modal-dialog modal-sm modal-notify modal-danger" role="document">
    <div class="modal-content text-center">
      <div class="modal-body">
        <div class="alert alert-warning">
          <h4>Confirmer la désactivation</h4>
          <p>
            {{ user.first_name }} {{ user.last_name }} ne pourra plus se connecter.
          </p>
          <div class="btn-list">
            <button class="btn btn-danger" type="button" data-dismiss="modal">OK</button>
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

  import UserDeactivate from "./UserDeactivate"

  export default Vue.extend({
    props: {
      user: Object,
      control: Object
    },
    methods: {
        modalId() {
            return 'modalDeactivateUser' + this.control.id + '-' + this.user.id
        }
    }
  })
</script>

<style></style>
