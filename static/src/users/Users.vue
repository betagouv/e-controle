<template>
<div class="card card-collapsed border-0 mb-0">
  <div class="card-header border-0 pl-0" data-toggle="card-collapse">
    <h5 class="card-title font-weight-bold"><a href="#"><i class="dropdown-icon fe fe-users"></i>Personnes ayant accès au contrôle</a></h5>
  </div>
  <div class="card-body">
    <div class="card">
      <div class="card-header pr-0">
        <div class="col">
          <h3 class="card-title"><i class="fa fa-institution mr-2"></i><strong>Équipe de contrôle</strong></h3>
        </div>
        <div class="col-auto">
          <button class="fe fe-plus btn btn-primary" data-toggle="modal" data-target="#addUserModal" @click="clickAddUser('inspector')"> Ajouter une personne</button>
        </div>
      </div>
      <user-list :users="inspectorUsers()" profile-type="inspector" :control="control"></user-list>
    </div>

    <div class="card">
      <div class="card-header pr-0">
        <div class="col">
          <h3 class="card-title"><i class="fe fe-user mr-2"></i><strong>Organisme controlé</strong></h3>
        </div>
        <div class="col-auto">
          <button class="fe fe-plus btn btn-primary" data-toggle="modal" data-target="#addUserModal" @click="clickAddUser('audited')"> Ajouter une personne</button>
        </div>
      </div>
      <user-list :users="auditedUsers()" profile-type="audited" :control="control"></user-list>
    </div>

    <div data-toggle="card-collapse" class="text-center bg-blue cursor-pointer text-white" style="cursor: pointer;"><i class="fe fe-chevron-up"></i></div>

  </div>
</div>
</template>

<script lang="ts">
  import axios from "axios"
  import Vue from "vue";
  import VueAxios from "vue-axios"

  import EventBus from '../events'
  import UserList from "./UserList"

  Vue.use(VueAxios, axios)

  export default Vue.extend({
    props: {
      control: Object,
      requestUserProfileType: String
    },
    data() {
      return {
        users: []
      }
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
      clickAddUser(profileType) {
        EventBus.$emit('click-add-user', {
          'control': this.control,
          'profileType': profileType
        })
      },
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
