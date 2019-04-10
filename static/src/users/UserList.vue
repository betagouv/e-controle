<template>
  <div class="card" v-if="getUserProfiles && getUserProfiles.length">
    <div class="card-header">
      <h3 v-if="profileType=='inspector'" class="card-title"><i class="fa fa-institution mr-2"></i><strong>Équipe de contrôle</strong></h3>
      <h3 v-if="profileType=='audited'" class="card-title"><i class="fe fe-user mr-2"></i><strong>Organisme controlé</strong></h3>
    </div>
    <div class="card-body o-auto" style="height: o-auto">
      <ul class="list-unstyled list-separated">
        <li class="list-separated-item" v-for="profile of getUserProfiles">
          <div class="row align-items-center">
            <div class="col-auto">
              <span class="avatar avatar-pink">{{ profile.user.first_name.charAt(0) }}{{ profile.user.last_name.charAt(0) }}</span>
            </div>
            <div class="col">
              <a href="javascript:void(0)" class="text-inherit" :title="profile.organization">{{ profile.user.first_name }} {{ profile.user.last_name }}</a>
              <small class="d-block item-except text-sm text-muted h-1x"><a :href="'mailto:' + profile.user.email">{{ profile.user.email }}</a></small>
            </div>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script lang="ts">
  import Vue from "vue";

  import axios from 'axios'
  import VueAxios from 'vue-axios'

  import { mapGetters } from 'vuex'
  import { store } from '../store/store';

  Vue.use(VueAxios, axios)



  export default Vue.extend({
    data: () {
      return {
      }
    },
    store,
    props: {
      profileType: String,
      controlId: String
    },
    computed: mapGetters([
      'getUserProfiles'
    ]),
    created() {
      this.$store.dispatch('loadData')
    }
  });
</script>

<style></style>
