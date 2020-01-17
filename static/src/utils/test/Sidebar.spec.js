import { createLocalVue, shallowMount } from '@vue/test-utils'
import { getField, updateField } from 'vuex-map-fields'

import { loadStatuses } from '../../store'
import Sidebar from '../Sidebar'
import Vuex from 'vuex'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('Sidebar.vue', () => {
  let store
  let wrapper
  let user
  let controls
  beforeEach(() => {
    jest.resetModules()
    jest.clearAllMocks()

    user = { id: 123, is_inspector: true, is_audited: false }
    controls = [{
      id: 345,
      title: 'Controle de Bloup',
      reference_code: '2020_bloup',
      depositing_organization: 'Mairie de Bloup',
      questionnaires: [
        {
          id: 678,
          is_draft: false,
          numbering: 3,
          title: 'On veut des réponses',
        },
        {
          id: 679,
          is_draft: true,
          numbering: 5,
          title: 'Sérieux on veut des réponses',
        },
      ],
    }]

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

  test('does not display on welcome pages', () => {
    const path = '/bienvenue/'
    const mockSetAttribute = jest.fn(() => {
      return [{
        setAttribute: () => {},
      }]
    })
    const mockWindow = {
      location: {
        pathname: path,
      },
      document: {
        getElementsByClassName: () => {
          return [{
            setAttribute: mockSetAttribute,
          }]
        },
      },
    }

    wrapper = shallowMount(
      Sidebar,
      {
        propsData: {
          window: mockWindow,
        },
        store,
        localVue,
      })

    store.commit('updateSessionUser', user)
    store.commit('updateSessionUserLoadStatus', loadStatuses.SUCCESS)

    store.commit('updateControls', controls)
    store.commit('updateControlsLoadStatus', loadStatuses.SUCCESS)

    // Width has been fixed
    expect(mockSetAttribute).toHaveBeenCalled()
    // Menu is not built, even though the data was succesfully fetched from store.
    expect(wrapper.vm.isMenuBuilt).toBeFalsy()
    expect(wrapper.vm.menu).toHaveLength(0)
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

    expect(controlMenuItem.child).toHaveLength(2)
    let questionnaireMenuItem = controlMenuItem.child[0]
    let questionnaire = controls[0].questionnaires[0]
    expect(questionnaireMenuItem.title).toEqual(
      expect.stringContaining(questionnaire.title))
    expect(questionnaireMenuItem.title).toEqual(
      expect.stringContaining('' + questionnaire.numbering))
    expect(questionnaireMenuItem.href).toEqual(
      expect.stringContaining('' + questionnaire.id))

    questionnaireMenuItem = controlMenuItem.child[1]
    questionnaire = controls[0].questionnaires[1]
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

  test('does not show drafts for audited user', () => {
    user.is_inspector = false
    user.is_audited = true
    expect(controls[0].questionnaires).toHaveLength(2)

    store.commit('updateSessionUser', user)
    store.commit('updateSessionUserLoadStatus', loadStatuses.SUCCESS)

    store.commit('updateControls', controls)
    store.commit('updateControlsLoadStatus', loadStatuses.SUCCESS)

    expect(wrapper.vm.isMenuBuilt).toBeTruthy()
    expect(wrapper.vm.menu).toHaveLength(1)

    const controlMenuItem = wrapper.vm.menu[0]
    expect(controlMenuItem.child).toHaveLength(1)
  })

  describe('uses appropriate href for questionnaires', () => {
    beforeEach(() => {
      store.commit('updateSessionUser', user)
      store.commit('updateSessionUserLoadStatus', loadStatuses.SUCCESS)
    })

    test('href for non-draft questionnaire', () => {
      const isDraft = false
      const editorId = user.id + 1
      const questionnaire = {
        id: 678,
        is_draft: isDraft,
        numbering: 3,
        title: 'On veut des réponses',
        editor: { id: editorId },
      }
      controls[0].questionnaires = [questionnaire]
      expect(controls[0].questionnaires[0].editor.id).not.toBe(user.id)

      store.commit('updateControls', controls)
      store.commit('updateControlsLoadStatus', loadStatuses.SUCCESS)

      expect(wrapper.vm.menu[0].child).toHaveLength(1)
      expect(wrapper.vm.menu[0].child[0].href).toEqual(
        expect.stringContaining('' + questionnaire.id))
      expect(wrapper.vm.menu[0].child[0].href).not.toEqual(expect.stringContaining('modifier'))
    })

    test('href for draft questionnaire if current user is editor', () => {
      const isDraft = true
      const editorId = user.id
      const questionnaire = {
        id: 678,
        is_draft: isDraft,
        numbering: 3,
        title: 'On veut des réponses',
        editor: { id: editorId },
      }
      controls[0].questionnaires = [questionnaire]
      expect(controls[0].questionnaires[0].editor.id).toBe(user.id)

      store.commit('updateControls', controls)
      store.commit('updateControlsLoadStatus', loadStatuses.SUCCESS)

      expect(wrapper.vm.menu[0].child).toHaveLength(1)
      expect(wrapper.vm.menu[0].child[0].href).toEqual(
        expect.stringContaining('' + questionnaire.id))
      expect(wrapper.vm.menu[0].child[0].href).toEqual(expect.stringContaining('modifier'))
    })

    test('href for draft questionnaire if current user is not editor', () => {
      const isDraft = true
      const editorId = user.id + 1
      const questionnaire = {
        id: 678,
        is_draft: isDraft,
        numbering: 3,
        title: 'On veut des réponses',
        editor: { id: editorId },
      }
      controls[0].questionnaires = [questionnaire]
      expect(controls[0].questionnaires[0].editor.id).not.toBe(user.id)

      store.commit('updateControls', controls)
      store.commit('updateControlsLoadStatus', loadStatuses.SUCCESS)

      expect(wrapper.vm.menu[0].child).toHaveLength(1)
      expect(wrapper.vm.menu[0].child[0].href).toEqual(
        expect.stringContaining('' + questionnaire.id))
      expect(wrapper.vm.menu[0].child[0].href).not.toEqual(expect.stringContaining('modifier'))
    })
  })
})
