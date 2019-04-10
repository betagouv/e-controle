import Vuex from 'vuex'
import Vue from "vue"
import axios from 'axios'
import VueAxios from 'vue-axios'

Vue.use(VueAxios, axios)
Vue.use(Vuex);


export const store = new Vuex.Store({
    state: {
      users: [],
    },

    mutations: {
      updateUsers(state, users) {
          state.users = users
      }
    },
    actions: {
      loadData({commit}) {
        axios.get('/api/user/').then((response) => {
          commit('updateUsers', response.data)
        })
      }
    },
    getters: {
        getAllUsers: state => {
            return state.users
        },
        getUsers: (state) => (controlId, profileType) => {
            return state.users.filter(u => {
                return (u.profile_type == profileType) && (u.controls.includes(controlId))
            })
        }
    }
})
