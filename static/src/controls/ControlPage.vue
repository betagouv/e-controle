<template>
  <div id="page-content" class="container">

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

    <video-modal
      id="fileExplorerVideoModal"
      :video-versions="[
        {
          url: staticFilesUrl + 'videos/file-explorer.mp4',
          type: 'video/mp4'
        },
        {
          url: staticFilesUrl + 'videos/file-explorer.webm',
          type: 'video/webm'
        },
      ]"
    >
    </video-modal>

  </div>
</template>

<script>
import Vue from 'vue'

import AddUserModal from '../users/AddUserModal'
import ControlCard from './ControlCard'
import NoControls from './NoControls'
import RemoveUserModal from '../users/RemoveUserModal'
import UpdateUserModal from '../users/UpdateUserModal'
import VideoModal from '../utils/VideoModal'

export default Vue.extend({
  props: [
    'controls',
    'user',
    'staticFilesUrl',
  ],
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
    VideoModal,
  },

})
</script>
