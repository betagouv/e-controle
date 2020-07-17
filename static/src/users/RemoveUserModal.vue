<template>
<div class="modal fade remove-user-modal"
     id="removeUserModal"
     tabindex="-1"
     role="dialog"
     aria-labelledby="removeUserModal"
     aria-hidden="true">
  <div class="modal-dialog modal-sm modal-notify modal-danger" role="document">
    <div class="modal-content text-center">
      <div class="modal-body">
        <div class="alert alert-warning">
          <h4>Confirmer la suppression</h4>
          <error-bar v-if="hasErrors" :noclose="true">
            La suppression d'utilisateur n'a pas fonctionné.
          </error-bar>
          <p>
            {{ editingUser.first_name }} {{ editingUser.last_name }}
            n'aura plus accès à cette procédure :
            {{ editingControl.title }}.
          </p>
          <div class="btn-list">
            <button @click="remove()" class="btn btn-danger" type="submit">
              Supprimer
            </button>
            <button @click="cancel()" class="btn btn-secondary" type="button" data-dismiss="modal">
              Annuler
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<script lang="ts">
import axios from 'axios'
import { mapFields } from 'vuex-map-fields'
import backend from '../utils/backend'
import Vue from 'vue'

import { store } from '../store'
import ErrorBar from '../utils/ErrorBar'
import EventBus from '../events'

export default Vue.extend({
  store,
  data: function() {
    return {
      postResult: {},
      hasErrors: false,
      error: undefined,
    }
  },
  components: {
    ErrorBar,
  },
  computed: {
    ...mapFields([
      'editingUser',
      'editingControl',
    ]),
  },
  methods: {
    cancel() {
      this.hasErrors = false
      this.error = undefined
    },
    remove() {
      this.hasErrors = false
      this.error = undefined

      var postData = { control: this.editingControl.id }
      axios.post(backend.removeUserFromControl(this.editingUser.id), postData)
        .then(response => {
          this.postResult = response.data
          EventBus.$emit('users-changed', this.postResult)
          $('#removeUserModal').modal('hide')
        })
        .catch(error => {
          this.hasErrors = true
          this.error = error
        })
    },
  },
})
</script>

<style></style>
