<template>
<div class="card-body" v-if="users && users.length">
  <ul class="list-unstyled list-separated">
    <li class="list-separated-item" v-for="(user, index) in users" :key="index">
      <div class="flex-row align-items-center">
        <div class="flex-column mr-4">
          <span class="avatar avatar-pink">{{ user.first_name.charAt(0) }}{{ user.last_name.charAt(0) }}</span>
        </div>
        <div class="flex-column mr-4 flex-grow-1">
          <div>{{ user.first_name }} {{ user.last_name }}</div>
          <small><a :href="'mailto:' + user.email">{{ user.email }}</a></small>
        </div>
        <slot name="user-buttons"></slot>
      </div>
    </li>
  </ul>
</div>
</template>

<script lang="ts">
  import { mapFields } from 'vuex-map-fields';
  import Vue from 'vue';
  import Vuex from 'vuex'

  import { store } from '../store'

  Vue.use(Vuex);

  export default Vue.extend({
    store,
    data: () {
      return {
        postResult: {}
      }
    },
    props: {
      users: Array,
      profileType: String,
      control: {
        type: Object,
        default: () => ({})
      },
    },
    computed: {
      ...mapFields([
        'editingUser',
        'editingControl'
        'sessionUser'
      ]),
    },
    methods: {
      updateEditingState(user) {
        this.editingControl = this.control
        this.editingUser = {}
        Object.assign(this.editingUser, user)
      }
    }
  });
</script>

<style></style>
