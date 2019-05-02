  import { getField, updateField } from 'vuex-map-fields';
import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);


export const store = new Vuex.Store({
    state: {
      editingControl: {},
      editingUser: {},
      editingProfileType: ''
    },
    getters: {
      getField,
    },
    mutations: {
      updateField,
    }
})
