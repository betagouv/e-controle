<template>
  <div class="card" v-if="users && users.length">
    <div class="card-header">
      <h3 v-if="profileType=='inspector'" class="card-title"><i class="fa fa-institution mr-2"></i><strong>Équipe de contrôle</strong></h3>
      <h3 v-if="profileType=='audited'" class="card-title"><i class="fe fe-user mr-2"></i><strong>Organisme controlé</strong></h3>
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
              <small class="d-block item-except text-sm text-muted h-1x"><a :href="'mailto:' + user.email">{{ user.email }}</a></small>
            </div>
            <div class="col-auto mr-4">
              <button class="fe fe-user-x btn btn-outline-warning" data-toggle="modal" :data-target="modalDeactivateUser"> Désactiver</button>
            </div>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script lang="ts">
  import Vue from "vue";

  export default Vue.extend({
    props: {
      users: Array,
      profileType: String
    }
  });
</script>

<style></style>
