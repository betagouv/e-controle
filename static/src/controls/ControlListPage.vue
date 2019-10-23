<template>
  <div>
    <div id="page-content" class="row row-cards">

      <control-list-sidebar :controls="controls" :hash="hash" :user="user">
      </control-list-sidebar>

      <div id="controls" class="col-lg-8">
        <control-list :controls="controls"
                      :user="user"
                      :webdavurl="webdavurl"
                      :hash="hash"
        >
        </control-list>
      </div>

      <add-user-modal></add-user-modal>

      <update-user-modal></update-user-modal>

      <remove-user-modal></remove-user-modal>

      <video-modal
        id="fileExplorerVideoModal"
        :video-url="staticFilesUrl + 'videos/file-explorer.mp4'"
        video-type="video/mp4"
      >
      </video-modal>

    </div>

  </div>
</template>

<script>
  import Vue from 'vue'

  import AddUserModal from "../users/AddUserModal"
  import ControlList from './ControlList'
  import ControlListSidebar from './ControlListSidebar'
  import RemoveUserModal from "../users/RemoveUserModal"
  import UpdateUserModal from "../users/UpdateUserModal"
  import VideoModal from "../utils/VideoModal"

  export default Vue.extend({
    props: [
      'controls',
      'user',
      'staticFilesUrl',
      'webdavurl',
    ],
    data: function() {
      return {
        hash: "",
      }
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
          // Change the hash to select the first control in the list, which will trigger the hashchange event again.
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
      ControlList,
      ControlListSidebar,
      RemoveUserModal,
      UpdateUserModal,
      VideoModal,
    },

  })
</script>