<template>
<div class="card card-collapsed border-0 mb-0">
  <div class="card-header border-0 pl-0" data-toggle="card-collapse">
    <h5 class="card-title font-weight-bold"><a href="#"><i class="dropdown-icon fe fe-users"></i>Personnes ayant accès au contrôle</a></h5>
  </div>
  <div class="card-body">

    <div class="card" v-if="requestUserProfileType==='inspector'">
      <button class="fe fe-plus btn btn-primary" data-toggle="modal" :data-target="'#modalAddUser' + controlId"> Ajouter une personne</button>
    </div>

    <user-list :users="inspectorUsers()" profile-type="inspector"></user-list>

    <user-list :users="auditedUsers()" profile-type="audited"></user-list>

    <div data-toggle="card-collapse" class="text-center bg-blue cursor-pointer text-white" style="cursor: pointer;"><i class="fe fe-chevron-up"></i></div>

    <user-create :control-id="controlId"></user-create>

  </div>
</div>
</template>

<script lang="ts">
  import axios from "axios"
  import Vue from "vue";
  import VueAxios from "vue-axios"

  import EventBus from '../events';
  import UserCreate from "./UserCreate"
  import UserList from "./UserList"

  Vue.use(VueAxios, axios)

  export default Vue.extend({
    props: {
      controlId: Number,
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
            controls: this.controlId
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
      }
    },
    mounted() {
      this.getUsers()
      EventBus.$on('user-added', data => {
        this.getUsers()
      })
    },
    components: {
      UserList,
      UserCreate
    }
  });
</script>

<style></style>
