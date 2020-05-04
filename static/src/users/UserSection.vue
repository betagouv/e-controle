<template>
  <div class="card">
    <div class="card-status card-status-top bg-blue"></div>
    <div class="card-header">
      <div class="card-title">
        <i class="fe fe-users mr-2"></i>
        <span>Qui a accès à cet espace ?</span>
      </div>
    </div>

    <div class="card-body">
      <div class="card">
        <div class="card-header justify-content-between">
          <h3 class="card-title">
            <i class="fa fa-university mr-2"></i>
            <strong>Équipe de contrôle</strong>
          </h3>
          <button v-if="sessionUser.is_inspector"
                  data-toggle="modal"
                  data-target="#addUserModal"
                  @click="updateEditingState('inspector')"
                  class="btn btn-primary">
            <i class="fe fe-plus"></i>
            Ajouter un contrôleur
          </button>
        </div>
        <user-list :users="inspectorUsers()" profile-type="inspector" :control="control">
        </user-list>
      </div>

      <div class="card mb-0">
        <div class="card-header justify-content-between">
          <h3 class="card-title">
            <i class="fa fa-building mr-2"></i>
            <strong>Organisme interrogé</strong>
          </h3>
          <button v-if="sessionUser.is_inspector"
                  data-toggle="modal"
                  data-target="#addUserModal"
                  @click="updateEditingState('audited')"
                  class="btn btn-primary">
            <i class="fe fe-plus"></i>
            Ajouter une personne
          </button>
        </div>
        <user-list :users="auditedUsers()" profile-type="audited" :control="control">
        </user-list>
      </div>
    </div>
  </div>

</template>

<script lang="ts">
import axios from 'axios'
import backendUrls from '../utils/backend'
import EventBus from '../events'
import { mapFields } from 'vuex-map-fields'
import { store } from '../store'
import UserList from './UserList'
import Vue from 'vue'

export default Vue.extend({
  store,
  props: {
    control: Object,
  },
  data() {
    return {
      users: [],
    }
  },
  computed: {
    ...mapFields([
      'editingControl',
      'editingProfileType',
      'sessionUser',
    ]),
  },
  methods: {
    getUsers() {
      axios.get(backendUrls.getUsersInControl(this.control.id))
        .then((response) => {
          this.users = response.data
        })
    },
    auditedUsers() {
      return this.users.filter(item => {
        return item.profile_type === 'audited'
      })
    },
    inspectorUsers() {
      return this.users.filter(item => {
        return item.profile_type === 'inspector'
      })
    },
    updateEditingState(profileType) {
      this.editingControl = this.control
      this.editingProfileType = profileType
    },
  },
  mounted() {
    this.getUsers()
    EventBus.$on('users-changed', () => {
      this.getUsers()
    })
  },
  components: {
    UserList,
  },
})
</script>

<style></style>
