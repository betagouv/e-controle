// Tests for the whole flow of questionnaire creation. These are not unit tests.

import { shallowMount, createLocalVue, mount } from '@vue/test-utils'

import axios from 'axios'
import { getField, updateField } from 'vuex-map-fields'
import { loadStatuses } from '../../store'
import QuestionnaireCreate from '../QuestionnaireCreate.vue'
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
      themes: [
        {
          id: 30948,
          description: 'my theme',
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

    // Mount, not shallowMount : this is not a unit test, so we want child components to be really
    // instantiated, not mocked out.
    wrapper = mount(
      QuestionnaireCreate,
      {
        propsData: {
          questionnaireId: questionnaireId,
        },
        store,
        localVue,
      })

    // Simulate store getting data from backend on app load.
    store.commit('updateControls', [{
      id: controlId,
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

  test('When annexe is added, it appears in the list of annexes', async () => {
    // Finish load by executing all the promises.
    await flushPromises

    // Before test : no files in annexe list.
    const question = wrapper.find('#theme-0-question-0')
    expect(question.findAll('.question-file').length).toBe(0)

    // Do file upload. We push the file object directly in the component's data (too complicated to
    // simulate real file upload)
    axios.post.mockImplementation((url, payload) => {
      return Promise.resolve({ data: payload })
    })
    const questionId = questionnaire.themes[0].questions[0].id
    const newFileId = 4987
    const file = {
      "id" : newFileId,
      "url" : "/fichier-question/" + newFileId + "/",
      "basename" : "2018-05-23_reponse_agence.png",
      "file" : "/media/JUG_2018_CNE_PARYS/Q03/ANNEXES-AUX-QUESTIONS/2018-05-23_reponse_agence.png",
      "question" : questionId,
    }
    expect(wrapper.find(QuestionFileUpload).exists()).toBe(true)
    const questionFileUpload = wrapper.find(QuestionFileUpload)
    questionFileUpload.vm.file = file
    questionFileUpload.vm.submitFile()
    expect(axios.post).toHaveBeenCalledWith(
      '/api/annexe/',
      expect.any(FormData),
      expect.any(Object))
    await flushPromises

    // Check the file appears in the annexe list.
    const questionAfter = wrapper.find('#theme-0-question-0')
    expect(questionAfter.findAll('.question-file').length).toBe(1)
  })
})