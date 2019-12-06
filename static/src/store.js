import axios from 'axios'
import backend from './utils/backend'
import { getField, updateField } from 'vuex-map-fields'
import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export const store = new Vuex.Store({
  state: {
    editingControl: {},
    editingUser: {},
    editingProfileType: '',
    sessionUser: {},
  },
  getters: {
    getField,
  },
  mutations: {
    updateField,
    updateSessionUser(state, user) {
      state.sessionUser = user
    },
  },
  actions: {
    fetchSessionUser({ commit }) {
      axios.get(backend.currentUser()).then((response) => {
        commit('updateSessionUser', response.data)
      }) // todo error case
    },
  },
})
