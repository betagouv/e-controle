<template>
  <div>
    <div class="mt-5 mb-5">
      <div class="flex-row justify-content-between">
        <div class="page-title">
          Accueil - Mes espaces de dépôt
        </div>
        <control-create v-if="user.is_inspector"></control-create>
      </div>
    </div>

    <div id="page-content" class="row row-cards">

      <control-list-sidebar :controls="controls" :hash="hash">
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
  import ControlCreate from "./ControlCreate"
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
      const updateHash = () => {
        console.debug('The hash has changed!', window.location.hash)
        if (window.location.hash === '' && this.controls.length > 0) {
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
      ControlCreate,
      ControlList,
      ControlListSidebar,
      RemoveUserModal,
      UpdateUserModal,
      VideoModal,
    },

  })
</script>