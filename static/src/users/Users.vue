<template>
<div class="card border-0 card-collapsed">
    <div class="card-header border-0" data-toggle="card-collapse">
        <div class="card-title">
            <i class="fe fe-users dropdown-icon"></i>
            <a href="#">Personnes ayant accès au contrôle</a>
        </div>
        <div class="card-options">
            <a href="#" class="card-options-collapse"><i class="fe fe-chevron-up"></i></a>
        </div>
    </div>
    <div class="card">
      <div class="card-header pr-0">
        <div class="col">
          <h3 class="card-title"><i class="fa fa-institution mr-2"></i><strong>Équipe de contrôle</strong></h3>
        </div>
        <div class="col-auto">
          <a v-if="sessionUser.is_inspector" href="" data-toggle="modal" data-target="#addUserModal" @click="updateEditingState('inspector')" class="btn btn-primary"><i class="fe fe-plus"></i>Ajouter un contrôleur</a>
        </div>
      </div>
      <user-list :users="inspectorUsers()" profile-type="inspector" :control="control"></user-list>
    </div>

    <div class="card">
      <div class="card-header pr-0">
        <div class="col">
          <h3 class="card-title"><i class="fe fe-user mr-2"></i><strong>Organisme contrôlé</strong></h3>
        </div>
        <div class="col-auto">
          <a v-if="sessionUser.is_inspector" href="" data-toggle="modal" data-target="#addUserModal" @click="updateEditingState('audited')" class="btn btn-primary"><i class="fe fe-plus"></i>Ajouter un contrôlé</a>
        </div>
      </div>
      <user-list :users="auditedUsers()" profile-type="audited" :control="control"></user-list>
    </div>

    <div data-toggle="card-collapse" class="text-center bg-blue cursor-pointer text-white" style="cursor: pointer;"><i class="fe fe-chevron-up"></i></div>

</div>
</template>

<script lang="ts">
  import { mapFields } from 'vuex-map-fields'
  import axios from "axios"
  import Vue from "vue";
  import VueAxios from "vue-axios"

  import { store } from '../store'
  import EventBus from '../events'
  import UserList from "./UserList"


  Vue.use(VueAxios, axios)


  export default Vue.extend({
    store,
    props: {
      control: Object,
    },
    data() {
      return {
        users: []
      }
    },
    computed: {
      ...mapFields([
        'editingControl'
        'editingProfileType',
        'sessionUser'
      ]),
    },
    methods: {
      getUsers() {
        Vue.axios.get('/api/user/', {
          params: {
            controls: this.control.id
          }
        }).then((response) => {
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
      }
    },
    mounted() {
      this.getUsers()
      EventBus.$on('users-changed', data => {
        this.getUsers()
      })
    },
    components: {
      UserList
    }
  });
</script>

<style></style>
