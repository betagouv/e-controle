import { getField, updateField } from 'vuex-map-fields';
import axios from 'axios'
import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);


export const store = new Vuex.Store({
    state: {
      editingControl: {},
      editingUser: {},
      editingProfileType: '',
      sessionUser: {},
      supportTeamEmail: 'bb'
    },
    getters: {
      getField,
    },
    mutations: {
      updateField,
      setSessionUser(state, user) {
          state.sessionUser = user
      }
    },
    actions: {
      setSessionUser({commit}) {
        axios.get('/api/user/current/').then((response) => {
          commit('setSessionUser', response.data)
        })
      }
    }
})
