import { createLocalVue, shallowMount } from '@vue/test-utils'
import { getField, updateField } from 'vuex-map-fields'

import { loadStatuses } from '../../store'
import Sidebar from '../Sidebar'
import Vuex from 'vuex'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('Sidebar.vue', () => {
  let store
  beforeEach(() => {
    store = new Vuex.Store({
      state: {
        controls: [],
        controlsLoadStatus: loadStatuses.LOADING,
        sessionUser: {},
        sessionUserLoadStatus: loadStatuses.LOADING,
      },
      getters: {
        getField,
      },
      mutations: {
        updateField,
      },
    })
  })

  test('is a Vue instance', () => {
    const wrapper = shallowMount(
      Sidebar,
      {
        store,
        localVue,
      })
    expect(wrapper.isVueInstance()).toBeTruthy()
  })
})
