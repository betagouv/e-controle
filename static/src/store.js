import axios from 'axios'
import { getField, updateField } from 'vuex-map-fields'
import backendUrls from './utils/backend.js'
import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export const loadStatuses = {
  LOADING: Symbol('LOADING'),
  SUCCESS: Symbol('SUCCESS'),
  ERROR: Symbol('ERROR'),
}

export const store = new Vuex.Store({
  state: {
    config: {},
    controls: [],
    controlsLoadStatus: loadStatuses.LOADING,
    currentQuestionnaire: {},
    editingControl: {},
    editingUser: {},
    editingProfileType: '',
    sessionUser: {},
    sessionUserLoadStatus: loadStatuses.LOADING,
  },
  getters: {
    getField,
  },
  mutations: {
    updateField,
    updateSessionUser(state, user) {
      state.sessionUser = user
    },
    updateSessionUserLoadStatus(state, newStatus) {
      state.sessionUserLoadStatus = newStatus
    },
    updateConfig(state, config) {
      state.config = config
    },
    updateControls(state, controls) {
      state.controls = controls
    },
    updateControlsLoadStatus(state, newStatus) {
      state.controlsLoadStatus = newStatus
    },
  },
  actions: {
    fetchConfig({ commit }) {
      axios.get(backendUrls.config()).then((response) => {
        commit('updateConfig', response.data)
      })
    },
    fetchSessionUser({ commit }) {
      axios.get(backendUrls.currentUser()).then((response) => {
        console.debug('Store got current user', response.data)
        commit('updateSessionUser', response.data)
        commit('updateSessionUserLoadStatus', loadStatuses.SUCCESS)
      }).catch(err => {
        console.error('Store got error fetching current user', err)
        commit('updateSessionUserLoadStatus', loadStatuses.ERROR)
      })
    },
    fetchControls({ commit }) {
      axios.get(backendUrls.control()).then(response => {
        console.debug('Store got controls', response.data)
        commit('updateControls', response.data)
        commit('updateControlsLoadStatus', loadStatuses.SUCCESS)
      }).catch(err => {
        console.error('Store got esrror fetching controls', err)
        commit('updateControlsLoadStatus', loadStatuses.ERROR)
      })
    },
  },
})
