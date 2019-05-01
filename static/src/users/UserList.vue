<template>
  <div class="card" v-if="users && users.length">
    <div v-if="profileType==='inspector'" class="card-header pr-0">
      <div class="col">
        <h3 class="card-title"><i class="fa fa-institution mr-2"></i><strong>Équipe de contrôle</strong></h3>
      </div>
      <div class="col-auto">
        <button class="fe fe-plus btn btn-primary" data-toggle="modal" data-target="#addUserModal" @click="clickAddUser()"> Ajouter une personne</button>
      </div>
    </div>
    <div v-if="profileType==='audited'" class="card-header pr-0">
      <div class="col">
        <h3 class="card-title"><i class="fe fe-user mr-2"></i><strong>Organisme controlé</strong></h3>
      </div>
      <div class="col-auto">
        <button class="fe fe-plus btn btn-primary" data-toggle="modal" data-target="#addUserModal" @click="clickAddUser()"> Ajouter une personne</button>
      </div>
    </div>

    <div class="card-body pr-0">
      <ul class="list-unstyled list-separated">
        <li class="list-separated-item" v-for="(user, index) in users" :key="index">
          <div class="row align-items-center">
            <div class="col-auto">
              <span class="avatar avatar-pink">{{ user.first_name.charAt(0) }}{{ user.last_name.charAt(0) }}</span>
            </div>
            <div class="col">
              <a href="javascript:void(0)" class="text-inherit" :title="user.organization">{{ user.first_name }} {{ user.last_name }}</a>
              <small class="d-block item-except h-1x"><a :href="'mailto:' + user.email">{{ user.email }}</a></small>
            </div>
            <div class="col-auto">
              <button class="fe fe-edit btn btn-outline-primary" title="Modifier" data-toggle="modal" data-target="#updateUserModal" @click="clickUpdateUser(user)"></button>
            </div>
            <div class="col-auto mr-3">
              <button class="fe fe-user-x btn btn-outline-primary" title="Désactiver" data-toggle="modal" :data-target="'#modalDeactivateUser' + control.id + '-' + user.id"></button>
            </div>
          </div>
          <user-deactivate :user="user" :control="control"></user-deactivate>
          <user-update :user="user" :control="control"></user-update>
        </li>
      </ul>
    </div>
  </div>
</template>

<script lang="ts">
  import Vue from "vue";

  import EventBus from '../events';
  import UserDeactivate from "./UserDeactivate"

  export default Vue.extend({
    data: () {
      return {
        postResult: {}
      }
    },
    props: {
      users: Array,
      profileType: String,
      control: Object,
    },
    components: {
      UserDeactivate
    },
    methods: {
      clickAddUser() {
        EventBus.$emit('click-add-user', {
          'control': this.control,
          'profileType': this.profileType
        })
      },
      clickUpdateUser(user) {
        EventBus.$emit('click-update-user', {
          'control': this.control,
          'user': user
        })
      },
    }
  });
</script>

<style></style>
