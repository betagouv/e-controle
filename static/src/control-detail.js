import '@babel/polyfill'

import Vuex, { mapActions } from 'vuex'
import Vue from 'vue/dist/vue.js'

import { store } from './store'
import ControlPage from './controls/ControlPage'

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
  render: h => h(
    ControlPage,
    {
      props: {
        controls: controls,
        user: user,
      },
    }),
  methods: {
    ...mapActions(['fetchConfig', 'fetchSessionUser']),

  },
  created() {
    this.fetchConfig()
    this.fetchSessionUser()
  },
})
