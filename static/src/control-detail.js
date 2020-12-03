import '@babel/polyfill'

import Vuex, { mapActions } from 'vuex'
import Vue from 'vue/dist/vue.js'

import ControlDetail from './controls/ControlDetail'
import { loadStatuses, store } from './store'

Vue.use(Vuex)

/*
XSS-safe way to get JSON data from server : write it to html (django template does html encoding)
and then fetch it into JS using safe DOM manipulation functions.
Source :
https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html#html-entity-encoding

A simpler safe way to get unsafe server data into Vue would be to get it through an AJAX request,
instead of passing it through server templates.
It does adds a delay for the user, since they will wait for the ajax-requested data.
*/
const controlsDataEl = document.getElementById('controls-data')
const userDataEl = document.getElementById('user-data')
// decode and parse the content of the div
const controls = JSON.parse(controlsDataEl.textContent)
const user = JSON.parse(userDataEl.textContent)

new Vue({ // eslint-disable-line no-new
  store,
  el: '#control-detail-vm',
  components: {
    ControlDetail,
  },
  methods: {
    ...mapActions(['fetchConfig', 'fetchControls']),
  },
  created() {
    // Ask the store to fetch the config from server and store it.
    this.fetchConfig()
    this.fetchControls()

    // Store the controls in the Vuex store, for use for other components (e.g. Sidebar)
    this.$store.commit('updateControls', controls)
    this.$store.commit('updateControlsLoadStatus', loadStatuses.SUCCESS)
    // Store the current user in the Vuex store, for use for other components (e.g. Sidebar)
    this.$store.commit('updateSessionUser', user)
    this.$store.commit('updateSessionUserLoadStatus', loadStatuses.SUCCESS)
  },
})
