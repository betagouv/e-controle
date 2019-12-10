import axios from 'axios'
import { getField, updateField } from 'vuex-map-fields'
import backendUrls from './utils/backend.js'
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
    config: {},
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
    updateConfig(state, config) {
      state.config = config
    },
  },
  actions: {
    loadConfig({ commit }) {
      axios.get(backendUrls.config()).then((response) => {
        commit('updateConfig', response.data)
      })
    },
    fetchSessionUser({ commit }) {
      axios.get(backendUrls.currentUser()).then((response) => {
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
