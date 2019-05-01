<template>
<div class="card-body pr-0" v-if="users && users.length">
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
          <button class="fe fe-user-x btn btn-outline-primary" title="Supprimer" data-toggle="modal" data-target="#removeUserModal" @click="clickRemoveUser(user)"></button>
        </div>
      </div>
    </li>
  </ul>
</div>
</template>

<script lang="ts">
  import Vue from "vue";

  import EventBus from '../events';

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
    methods: {
      clickUpdateUser(user) {
        EventBus.$emit('click-update-user', {
          'control': this.control,
          'user': user
        })
      },
      clickRemoveUser(user) {
        EventBus.$emit('click-remove-user', {
          'control': this.control,
          'user': user
        })
      }
    }
  });
</script>

<style></style>
