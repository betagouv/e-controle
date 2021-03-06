<template>
  <div id="page-content" class="mx-3">

    <div id="controls">
      <div v-if="controls.length === 0">
        <no-controls v-if="user.is_inspector">
        </no-controls>
        <div v-else class="card">
          <div class="card-body">
            Vous n'avez accès à aucun espace de dépôt. Si vous avez besoin d'un accès, contactez
            l'équipe de contrôle.
          </div>
        </div>
      </div>

      <template v-else>
        <control-card v-if="displayedControl !== undefined"
                      :key="displayedControl.id"
                      :control="displayedControl"
                      :user="user"
        >
        </control-card>
      </template>
    </div>

    <add-user-modal></add-user-modal>

    <update-user-modal></update-user-modal>

    <remove-user-modal></remove-user-modal>

  </div>
</template>

<script>
import Vue from 'vue'

import AddUserModal from '../users/AddUserModal'
import ControlCard from './ControlCard'
import { mapState } from 'vuex'
import NoControls from './NoControls'
import RemoveUserModal from '../users/RemoveUserModal'
import UpdateUserModal from '../users/UpdateUserModal'

export default Vue.extend({
  name: 'ControlPage',
  data: function() {
    return {
      hash: '',
    }
  },
  computed: {
    displayedControl() {
      return this.controls.find(control => {
        return this.hash === '#control-' + control.id
      })
    },
    ...mapState({
      // Note : we don't map sessionUserLoadStatus and controlsLoadStatus, because the only use of
      // ControlPage is within a page which pre-fetches the data from server, so we know it is
      // already there.
      user: 'sessionUser',
      controls: 'controls',
    }),
  },
  mounted() {
    const isValidHash = (hash) => {
      const reg = /^#control-[0-9]+$/
      return reg.test(hash)
    }

    const hashPointsToExistingControl = (hash) => {
      if (!isValidHash(hash)) {
        return false
      }
      const controlId = parseInt(hash.replace('#control-', ''), 10)
      if (isNaN(controlId)) {
        return false
      }
      return this.controls.map(control => control.id).includes(controlId)
    }

    const updateHash = () => {
      console.debug('hashchange', window.location.hash)
      if (!hashPointsToExistingControl(window.location.hash) && this.controls.length > 0) {
        // Change the hash to select the first control in the list, which will trigger the
        // hashchange event again.
        window.location.hash = '#control-' + this.controls[0].id
        return
      }
      this.hash = window.location.hash
    }

    window.addEventListener(
      'hashchange',
      updateHash,
      false)

    updateHash()
  },
  components: {
    AddUserModal,
    ControlCard,
    NoControls,
    RemoveUserModal,
    UpdateUserModal,
  },

})
</script>
