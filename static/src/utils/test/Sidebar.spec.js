import { createLocalVue, shallowMount } from '@vue/test-utils'
import { getField, updateField } from 'vuex-map-fields'

import { loadStatuses } from '../../store'
import Sidebar from '../Sidebar'
import Vuex from 'vuex'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('Sidebar.vue', () => {
  const user = { id: 123, is_inspector: true }
  const controls = [{
    id: 345,
    title: 'Controle de Bloup',
    reference_code: '2020_bloup',
    depositing_organization: 'Mairie de Bloup',
    questionnaires: [{
      id: 678,
      is_draft: false,
      numbering: 3,
      title: 'On veut des réponses',
    }],
  }]

  let store
  let wrapper
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
        updateControls(state, controls) {
          state.controls = controls
        },
        updateControlsLoadStatus(state, newStatus) {
          state.controlsLoadStatus = newStatus
        },
        updateSessionUser(state, user) {
          state.sessionUser = user
        },
        updateSessionUserLoadStatus(state, newStatus) {
          state.sessionUserLoadStatus = newStatus
        },
      },
    })

    wrapper = shallowMount(
      Sidebar,
      {
        store,
        localVue,
      })
  })

  test('is a Vue instance', () => {
    expect(wrapper.isVueInstance()).toBeTruthy()
  })

  test('shows menu', () => {
    store.commit('updateSessionUser', user)
    store.commit('updateSessionUserLoadStatus', loadStatuses.SUCCESS)

    store.commit('updateControls', controls)
    store.commit('updateControlsLoadStatus', loadStatuses.SUCCESS)

    expect(wrapper.vm.isMenuBuilt).toBeTruthy()

    expect(wrapper.vm.menu).toHaveLength(1)
    const controlMenuItem = wrapper.vm.menu[0]
    expect(controlMenuItem.title).toEqual(
      expect.stringContaining(controls[0].reference_code))
    expect(controlMenuItem.title).toEqual(
      expect.stringContaining(controls[0].depositing_organization))
    expect(controlMenuItem.href).toEqual(expect.stringContaining('' + controls[0].id))

    expect(controlMenuItem.child).toHaveLength(1)
    const questionnaireMenuItem = controlMenuItem.child[0]
    const questionnaire = controls[0].questionnaires[0]
    expect(questionnaireMenuItem.title).toEqual(
      expect.stringContaining(questionnaire.title))
    expect(questionnaireMenuItem.title).toEqual(
      expect.stringContaining('' + questionnaire.numbering))
    expect(questionnaireMenuItem.href).toEqual(
      expect.stringContaining('' + questionnaire.id))
  })

  test('shows error if controls are not fetched', () => {
    store.commit('updateSessionUser', user)
    store.commit('updateSessionUserLoadStatus', loadStatuses.SUCCESS)

    store.commit('updateControlsLoadStatus', loadStatuses.ERROR)

    expect(wrapper.vm.isMenuBuilt).toBeFalsy()
    expect(wrapper.vm.menu).toHaveLength(0)

    expect(wrapper.vm.hasError).toBeTruthy()
    expect(wrapper.vm.errorMessage).not.toBeUndefined()

    // Error message is displayed in error-bar
    expect(wrapper.find('#sidebar-error-bar').isVisible()).toBeTruthy()
    expect(wrapper.find('#sidebar-error-bar').element.innerHTML).toEqual(
      expect.stringContaining(wrapper.vm.errorMessage))
  })

  test('shows error if user is not fetched', () => {
    store.commit('updateSessionUserLoadStatus', loadStatuses.ERROR)

    store.commit('updateControls', controls)
    store.commit('updateControlsLoadStatus', loadStatuses.SUCCESS)

    expect(wrapper.vm.isMenuBuilt).toBeFalsy()
    expect(wrapper.vm.menu).toHaveLength(0)

    expect(wrapper.vm.hasError).toBeTruthy()
    expect(wrapper.vm.errorMessage).not.toBeUndefined()

    // Error message is displayed in error-bar
    expect(wrapper.find('#sidebar-error-bar').isVisible()).toBeTruthy()
    expect(wrapper.find('#sidebar-error-bar').element.innerHTML).toEqual(
      expect.stringContaining(wrapper.vm.errorMessage))
  })

  test('does not display on welcome pages', () => {
    // Mock out window.location.pathname
    global.window = Object.create(window)
    const path = '/bienvenue/'
    Object.defineProperty(window, 'location', {
      value: {
        pathname: path,
      },
    })
    expect(window.location.pathname).toEqual(path)

    // Mock out document.getElementsByClassName, used to fix sidebar width
    const spy = jest.spyOn(document, 'getElementsByClassName')
    document.getElementsByClassName.mockImplementation(() => {
      return [{
        setAttribute: () => {},
      }]
    })

    const wrapper = shallowMount(
      Sidebar,
      {
        store,
        localVue,
      })

    store.commit('updateSessionUser', user)
    store.commit('updateSessionUserLoadStatus', loadStatuses.SUCCESS)

    store.commit('updateControls', controls)
    store.commit('updateControlsLoadStatus', loadStatuses.SUCCESS)

    // Width has been fixed
    expect(spy).toHaveBeenCalled()
    // Menu is not built, even though the data was succesfully fetched from store.
    expect(wrapper.vm.isMenuBuilt).toBeFalsy()
    expect(wrapper.vm.menu).toHaveLength(0)
  })
})
