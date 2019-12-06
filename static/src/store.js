import axios from 'axios'
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
    setSessionUser(state, user) {
      state.sessionUser = user
    },
  },
  actions: {
    setSessionUser({ commit }) {
      axios.get('/api/user/current/').then((response) => {
        commit('setSessionUser', response.data)
      })
    },
  },
})
