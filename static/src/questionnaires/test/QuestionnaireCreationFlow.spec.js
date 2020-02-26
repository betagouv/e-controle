// Tests for the whole flow of questionnaire creation. These are not unit tests.

import { createLocalVue, mount } from '@vue/test-utils'
import { when, resetAllWhenMocks } from 'jest-when'

import axios from 'axios'
import { getField, updateField } from 'vuex-map-fields'
import { loadStatuses } from '../../store'
import QuestionnaireCreate from '../QuestionnaireCreate.vue'
import QuestionFileList from '../../questions/QuestionFileList'
import QuestionFileUpload from '../../questions/QuestionFileUpload'
import Vuex from 'vuex'
import flushPromises from 'flush-promises'

jest.mock('axios')
const localVue = createLocalVue()
localVue.use(Vuex)

describe('Questionnaire creation flow', () => {
  let store
  let wrapper
  let questionnaire

  beforeEach(() => {
    // Setup the questionnaire creation page.
    jest.resetModules()
    jest.clearAllMocks()
    resetAllWhenMocks()

    store = new Vuex.Store({
      state: {
        controls: [],
        controlsLoadStatus: loadStatuses.LOADING,
        currentQuestionnaire: {},
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
      },
    })

    questionnaire = {
      control: 5678,
      id: 1234,
      title: 'Le questionnaire, c\'est super',
      description: 'Répondez aux questions pom pom',
      themes: [
        {
          id: 30948,
          title: 'my theme',
          questions: [
            {
              id: 20947,
              description: 'my question',
              question_files: [],
            },
          ],
        },
      ],
      is_draft: true,
    }

    // Mock axios : save questionnaire
    when(axios.put).calledWith('/api/questionnaire/' + questionnaire.id + '/')
      .mockImplementation((url, payload) => {
        return Promise.resolve({ data: payload })
      })

    // Mount, not shallowMount : this is not a unit test, so we want child components to be really
    // instantiated, not mocked out.
    wrapper = mount(
      QuestionnaireCreate,
      {
        propsData: {
          questionnaireId: questionnaire.id,
        },
        store,
        localVue,
      })

    // Simulate store getting data from backend on app load.
    store.commit('updateControls', [{
      id: questionnaire.control,
      questionnaires: [
        questionnaire,
      ],
    }])
    store.commit('updateControlsLoadStatus', loadStatuses.SUCCESS)
  })

  afterEach(() => {
    // If we removed error output in previous test, set it back for next test.
    if (console.error.mockRestore) {
      console.error.mockRestore()
    }
  })

  const uploadFile = (wrapper, filename) => {
    // Do file upload. We push the file object directly in the component's data (too complicated to
    // simulate real file upload)
    const questionId = questionnaire.themes[0].questions[0].id
    const newFileId = 4987
    const file = {
      id: newFileId,
      url: '/fichier-question/' + newFileId + '/',
      basename: filename,
      file: '/media/JUG_2018_CNE_PARYS/Q03/ANNEXES-AUX-QUESTIONS/' + filename,
      question: questionId,
    }
    when(axios.post).calledWith(
      '/api/annexe/',
      expect.any(FormData),
      expect.any(Object),
    ).mockImplementation((url, payload) => {
      return Promise.resolve({ data: file })
    })

    expect(wrapper.find(QuestionFileUpload).exists()).toBe(true)
    const questionFileUpload = wrapper.find(QuestionFileUpload)
    questionFileUpload.vm.file = file
    questionFileUpload.vm.submitFile()
    expect(axios.post).toHaveBeenCalledWith(
      '/api/annexe/',
      expect.any(FormData),
      expect.any(Object))
  }

  test('When annexe is added, it appears in the list of annexes', async () => {
    // Finish load by executing all the promises.
    await flushPromises
    await wrapper.vm.$forceUpdate() // force the update of the HTML of the Vue components
    expect(wrapper.find('#questionnaire-metadata-create').isVisible()).toBeTruthy()

    // Move to body create page.
    wrapper.find('#next-button').trigger('click')
    await wrapper.vm.$forceUpdate() // force the update of the HTML of the Vue components
    await flushPromises
    await wrapper.vm.$forceUpdate() // force the update of the HTML of the Vue components
    expect(wrapper.find('#questionnaire-body-create').isVisible()).toBeTruthy()

    // Before test : no files in annexe list.
    const bodyCreatePage = wrapper.find('#questionnaire-body-create')
    const question = bodyCreatePage.find('#theme-0-question-0')
    expect(question.findAll('.question-file')).toHaveLength(0)

    const filename = 'myfile.xls'
    uploadFile(wrapper, filename)
    await flushPromises // Make sure the axios call has returned
    await wrapper.vm.$forceUpdate() // force the update of the HTML of the Vue components

    // Check the file appears in the annexe list.
    const bodyCreatePageAfter = wrapper.find('#questionnaire-body-create')
    const questionAfter = bodyCreatePageAfter.find('#theme-0-question-0')
    const annexes = questionAfter.findAll('.question-file')
    expect(annexes).toHaveLength(1) // 0! Yet the currentQuestionnaire object contains the new annex
    expect(annexes.at(0).html()).toEqual(expect.stringContaining(filename))
  })

  test('When annexe is added, it appears in the Preview page (3rd step of wizard)', async () => {
    // Finish load by executing all the promises and force-refreshing the html.
    await flushPromises

    // Move to body create page.
    wrapper.find('#next-button').trigger('click')
    await wrapper.vm.$forceUpdate() // force the update of the HTML of the Vue components
    await flushPromises
    await wrapper.vm.$forceUpdate() // force the update of the HTML of the Vue components
    expect(wrapper.find('#questionnaire-body-create').isVisible()).toBeTruthy()

    // Before test : no files in annexe list in Preview page.
    const previewPage = wrapper.find('#questionnaire-preview')
    const question = previewPage.find('#question1-1')
    expect(question.findAll('.question-file')).toHaveLength(0)

    // Upload the file
    const filename = 'myfile.xls'
    uploadFile(wrapper, filename)
    await flushPromises

    // Move to preview page.
    wrapper.find('#next-button').trigger('click')
    await flushPromises
    expect(wrapper.find('#questionnaire-preview').isVisible()).toBeTruthy()
    await wrapper.vm.$forceUpdate() // force the update of the HTML of the Vue components

    // Check the file appears in the annexe list in Preview.
    const previewPageAfter = wrapper.find('#questionnaire-preview')
    const questionAfter = previewPageAfter.find('#question1-1')
    const annexes = questionAfter.findAll('.question-file')
    expect(annexes).toHaveLength(1)
    expect(annexes.at(0).html()).toEqual(expect.stringContaining(filename))
  })
})
