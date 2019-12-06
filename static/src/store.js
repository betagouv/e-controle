import axios from 'axios'
import backend from './utils/backend'
import { getField, updateField } from 'vuex-map-fields'
import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const loadStatuses = {
  LOADING: 'LOADING',
  SUCCESS: 'SUCCESS',
  ERROR: 'ERROR',
}

export const store = new Vuex.Store({
  state: {
    editingControl: {},
    editingUser: {},
    editingProfileType: '',
    sessionUser: {},
    loadStatus: loadStatuses.LOADING,
  },
  getters: {
    getField,
  },
  mutations: {
    updateField,
    updateSessionUser(state, user) {
      state.sessionUser = user
    },
    updateLoadStatus(state, newStatus) {
      state.loadStatus = newStatus
    },
  },
  actions: {
    fetchSessionUser({ commit }) {
      axios.get(backend.currentUser()).then((response) => {
        console.debug('Got current user', response.data)
        commit('updateSessionUser', response.data)
        commit('updateLoadStatus', loadStatuses.SUCCESS)
      }).catch(err => {
        console.error('Error fetching current user', err)
        commit('updateLoadStatus', loadStatuses.ERROR)
      })
    },
  },
})
