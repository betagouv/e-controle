<template>
<div class="card card-collapsed border-0 mb-0">
  <div class="card-header border-0 pl-0" data-toggle="card-collapse">
    <h5 class="card-title font-weight-bold"><a href="#"><i class="dropdown-icon fe fe-users"></i>Personnes ayant accès au contrôle</a></h5>
  </div>
  <div class="card-body">

    <div class="card">
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
  import Vue from "vue";
  import axios from "axios"
  import VueAxios from "vue-axios"

  import UserList from "./UserList.vue"
  import UserCreate from "./UserCreate.vue"

  Vue.use(VueAxios, axios)

  export default Vue.extend({
    props: {
      controlId: Number
    },
    data() {
      return {
        users: []
      }
    },
    methods: {
      getUsers() {
        var urlParams = new URLSearchParams()
        urlParams.set("controls", this.controlId)
        Vue.axios.get('/api/user/?' + urlParams.toString()).then((response) => {
          this.users = response.data
        })
      },
      auditedUsers() {
        return this.users.filter(item => {
           return item.profile_type == 'audited'
        })
      },
      inspectorUsers() {
        return this.users.filter(item => {
           return item.profile_type == 'inspector'
        })
      }
    },
    mounted() {
      this.getUsers()
    },
    components: {
      UserList,
      UserCreate
    }
  });
</script>

<style></style>
