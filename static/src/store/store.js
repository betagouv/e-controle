import Vuex from 'vuex'
import Vue from "vue"
import axios from 'axios'
import VueAxios from 'vue-axios'

Vue.use(VueAxios, axios)
Vue.use(Vuex);


export const store = new Vuex.Store({
    state: {
      userProfiles: []
    },
    actions: {
      loadData({commit}) {
        axios.get('/api/user/').then((response) => {
          commit('updateUserProfiles', response.data)
        })
      }
    },
    mutations: {
      updateUserProfiles(state, userProfiles) {
          state.userProfiles = userProfiles
      }
    },
    getters: {
        getUserProfiles: state => {
            return state.userProfiles
        }
    }
})
