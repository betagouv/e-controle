import axios from 'axios'
import { shallowMount, createLocalVue } from '@vue/test-utils'
import { getField, updateField } from 'vuex-map-fields'
import QuestionnaireCreate from '../QuestionnaireCreate.vue'
import Vuex from 'vuex'
import { loadStatuses } from '../../store'
import testUtils from '../../utils/testUtils'
import flushPromises from 'flush-promises'

jest.mock('axios')
const localVue = createLocalVue()
localVue.use(Vuex)

describe('QuestionnaireCreate.vue', () => {
  let store

  beforeEach(() => {
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
  })

  afterEach(() => {
    // If we removed error output in previous test, set it back for next test.
    if (console.error.mockRestore) {
      console.error.mockRestore()
    }
  })

  test('is a Vue instance', () => {
    const wrapper = shallowMount(
      QuestionnaireCreate,
      {
        propsData: {
          controlId: 1,
        },
        store,
        localVue,
      })
    expect(wrapper.isVueInstance()).toBeTruthy()
  })

  test('crashes without a controlId or questionnaireId', () => {
    // Remove error output, since we expect an error. Avoids clutter in test log.
    jest.spyOn(console, 'error')
    console.error.mockImplementation(() => {})

    expect(() => {
      shallowMount(
        QuestionnaireCreate,
        {
          propsData: {
            // no controlId or questionnaireId
          },
          store,
          localVue,
        })
    }).toThrow()
  })

  describe('create new questionnaire', () => {
    test('sets up without crashing', () => {
      expect(() => {
        shallowMount(
          QuestionnaireCreate,
          {
            propsData: {
              controlId: 1,
            },
            store,
            localVue,
          })
      }).not.toThrow()
    })

    test('sets currrentQuestionnaire into store', async () => {
      const controlId = 1

      shallowMount(
        QuestionnaireCreate,
        {
          propsData: {
            controlId: 1,
          },
          store,
          localVue,
        })

      store.commit('updateControls', [{ id: controlId }])
      store.commit('updateControlsLoadStatus', loadStatuses.SUCCESS)

      await flushPromises()

      expect(store.state.currentQuestionnaire.control).toBe(controlId)
      expect(store.state.currentQuestionnaire.description).not.toEqual('')
    })

    test('moves to first step of wizard', async () => {
      const controlId = 1

      const wrapper = shallowMount(
        QuestionnaireCreate,
        {
          propsData: {
            controlId: 1,
          },
          store,
          localVue,
        })

      store.commit('updateControls', [{ id: controlId }])
      store.commit('updateControlsLoadStatus', loadStatuses.SUCCESS)

      await flushPromises()

      expect(wrapper.vm.state).toEqual(1)

      assert(wrapper.find('#questionnaire-metadata-create').isVisible())
      assert(!wrapper.find('#questionnaire-body-create').isVisible())
      assert(!wrapper.find('#questionnaire-preview').isVisible())

      assert(wrapper.find('#wizard').props().activeStepNumber === 1)
    })
  })

  describe('update existing questionnaire', () => {
    test('sets up without crashing', () => {
      const questionnaireId = 1

      expect(() => {
        shallowMount(
          QuestionnaireCreate,
          {
            propsData: {
              questionnaireId: questionnaireId,
            },
            store,
            localVue,
          })
      }).not.toThrow()
    })

    test('sets currrentQuestionnaire into store', async () => {
      const questionnaireId = 1234
      const controlId = 5678
      const questionnaire = {
        control: controlId,
        id: questionnaireId,
        is_draft: true,
      }

      shallowMount(
        QuestionnaireCreate,
        {
          propsData: {
            questionnaireId: questionnaireId,
          },
          store,
          localVue,
        })

      store.commit('updateControls', [{
        id: controlId,
        questionnaires: [
          questionnaire,
        ],
      }])
      store.commit('updateControlsLoadStatus', loadStatuses.SUCCESS)

      await flushPromises()

      expect(store.state.currentQuestionnaire).toBe(questionnaire)
    })

    describe('displays error', () => {
      test('if cannot get questionnaire from store', async () => {
        jest.spyOn(console, 'error')
        console.error.mockImplementation(() => {})

        const questionnaireId = 1234

        const wrapper = shallowMount(
          QuestionnaireCreate,
          {
            propsData: {
              questionnaireId: questionnaireId,
            },
            store,
            localVue,
          })

        store.commit('updateControlsLoadStatus', loadStatuses.ERROR)

        await flushPromises()

        expect(store.state.currentQuestionnaire).toEqual({})

        assert(wrapper.vm.errorMessage !== '')
        assert(wrapper.vm.hasErrors)
        assert(wrapper.find('#questionnaire-create-error').exists())

        assert(!wrapper.find('#questionnaire-metadata-create').isVisible())
        assert(!wrapper.find('#questionnaire-body-create').isVisible())
        assert(!wrapper.find('#questionnaire-preview').isVisible())
      })

      test('if questionnaire is not a draft', async () => {
        jest.spyOn(console, 'error')
        console.error.mockImplementation(() => {})

        const questionnaireId = 1234
        const controlId = 5678
        const questionnaire = {
          control: controlId,
          id: questionnaireId,
          is_draft: false,
        }

        const wrapper = shallowMount(
          QuestionnaireCreate,
          {
            propsData: {
              questionnaireId: questionnaireId,
            },
            store,
            localVue,
          })

        store.commit('updateControls', [{
          id: controlId,
          questionnaires: [
            questionnaire,
          ],
        }])
        store.commit('updateControlsLoadStatus', loadStatuses.SUCCESS)

        await flushPromises()

        expect(store.state.currentQuestionnaire).toEqual({})

        assert(wrapper.vm.errorMessage !== '')
        assert(wrapper.vm.hasErrors)
        assert(wrapper.find('#questionnaire-create-error').exists())

        assert(!wrapper.find('#questionnaire-metadata-create').isVisible())
        assert(!wrapper.find('#questionnaire-body-create').isVisible())
        assert(!wrapper.find('#questionnaire-preview').isVisible())
      })
    })

    test('moves to first step of wizard', async () => {
      const questionnaireId = 1234
      const controlId = 5678
      const questionnaire = {
        control: controlId,
        id: questionnaireId,
        is_draft: true,
      }

      const wrapper = shallowMount(
        QuestionnaireCreate,
        {
          propsData: {
            questionnaireId: questionnaireId,
          },
          store,
          localVue,
        })

      store.commit('updateControls', [{
        id: controlId,
        questionnaires: [
          questionnaire,
        ],
      }])
      store.commit('updateControlsLoadStatus', loadStatuses.SUCCESS)

      await flushPromises()

      expect(wrapper.vm.state).toEqual(1)

      assert(wrapper.find('#questionnaire-metadata-create').isVisible())
      assert(!wrapper.find('#questionnaire-body-create').isVisible())
      assert(!wrapper.find('#questionnaire-preview').isVisible())

      assert(wrapper.find('#wizard').props().activeStepNumber === 1)
    })
  })

  describe('Publishing flow', () => {
    let wrapper
    let questionnaire
    beforeEach(async () => {
      // Setup component to load existing questionnaire
      const questionnaireId = 1234
      const controlId = 5678
      questionnaire = {
        control: controlId,
        id: questionnaireId,
        is_draft: true,
      }

      wrapper = shallowMount(
        QuestionnaireCreate,
        {
          propsData: {
            questionnaireId: questionnaireId,
          },
          store,
          localVue,
        })

      store.commit('updateControls', [{
        id: controlId,
        questionnaires: [
          questionnaire,
        ],
      }])
      store.commit('updateControlsLoadStatus', loadStatuses.SUCCESS)

      await flushPromises()

      // Move to state 3 : ready to publish
      wrapper.vm.state = 3
    })

    test('Displays the questionnaire-preview component', () => {
      expect(wrapper.find('#questionnaire-metadata-create').isVisible()).toBeFalsy()
      expect(wrapper.find('#questionnaire-body-create').isVisible()).toBeFalsy()
      expect(wrapper.find('#questionnaire-preview').isVisible()).toBeTruthy()
    })

    test('shows publishConfirmModal when Publish button is clicked', async () => {
      wrapper.find('#publishButton').trigger('click')

      expect(testUtils.isModalShowing(wrapper, '#publishConfirmModal')).toBeTruthy()
    })

    test('shows savingModal when publishing is confirmed', async () => {
      wrapper.vm.$refs.publishConfirmModal.$emit('confirm')

      expect(testUtils.isModalShowing(wrapper, '#savingModal')).toBeTruthy()
    })

    test('calls publish api when publishing is confirmed', () => {
      wrapper.vm.$refs.publishConfirmModal.$emit('confirm')

      // PUT is called, because it's an update of an existing questionnaire.
      expect(axios.put).toHaveBeenCalledWith(
        '/api/questionnaire/' + questionnaire.id + '/',
        questionnaire)
    })

    test('shows success modal when publish happened successfully', async () => {
      // Mock out wait function to resolve immediately without wait.
      wrapper.vm.wait = () => Promise.resolve()
      // Mock out axios to return with sucess
      axios.post.mockResolvedValue({})

      wrapper.vm.$refs.publishConfirmModal.$emit('confirm')

      // Resolve all promises
      await flushPromises()

      assert(testUtils.isModalShowing(wrapper, '#savedModal'))
    })

    test('displays errors when publish api returned errors', async () => {
      jest.spyOn(console, 'error')
      console.error.mockImplementation(() => {})

      // Mock axios to return publish error
      const error = { error: 'I am not happpyyyy', details: ['stuff', 'more stuff'] }
      axios.put.mockRejectedValue(error)

      wrapper.vm.$refs.publishConfirmModal.$emit('confirm')
      // Resolve all promises
      await flushPromises()

      expect(wrapper.vm.publishError).toEqual(error)

      // Intermediate modal is gone
      expect(testUtils.isModalShowing(wrapper, '#savingModal')).toBeFalsy()
      // Success modal not displayed
      expect(testUtils.isModalShowing(wrapper, '#savedModal')).toBeFalsy()
      // Initial modal is back
      expect(testUtils.isModalShowing(wrapper, '#publishConfirmModal')).toBeTruthy()

      // Modal has the error passed in props
      expect(wrapper.find('#publishConfirmModal').props().error).toEqual(error)
    })
  })

  describe('Navigation', () => {
    let wrapper
    const controlId = 1
    let mockWindow
    beforeEach(() => {
      mockWindow = {
        location: {
          href: '',
        },
      }
      wrapper = shallowMount(
        QuestionnaireCreate,
        {
          propsData: {
            controlId: controlId,
            window: mockWindow,
          },
          store,
          localVue,
        })
      store.commit('updateControls', [{ id: controlId }])
      store.commit('updateControlsLoadStatus', loadStatuses.SUCCESS)
    })

    test('Saves draft before returning home', async () => {
      // Spy on form validation to make it pass
      jest.spyOn(wrapper.vm, 'validateCurrentForm')
      wrapper.vm.validateCurrentForm.mockImplementation(() => true)
      // Mock axios to return the questionnaire it got in argument
      axios.post.mockImplementation((url, payload) => {
        return Promise.resolve({ data: payload })
      })
      await flushPromises()

      wrapper.find('#go-home-button').trigger('click')
      await flushPromises()

      expect(wrapper.vm.validateCurrentForm).toHaveBeenCalled()
      expect(axios.post).toHaveBeenCalledWith(
        '/api/questionnaire/',
        expect.any(Object))
      expect(mockWindow.location.href).not.toEqual('')
    })

    test('If draft save fails, return home anyway', async () => {
      // Spy on form validation to make it pass
      jest.spyOn(wrapper.vm, 'validateCurrentForm')
      wrapper.vm.validateCurrentForm.mockImplementation(() => true)
      // Mock axios to fail save
      axios.post.mockRejectedValue({})
      await flushPromises()

      wrapper.find('#go-home-button').trigger('click')
      await flushPromises()

      expect(wrapper.vm.validateCurrentForm).toHaveBeenCalled()
      expect(axios.post).toHaveBeenCalledWith(
        '/api/questionnaire/',
        expect.any(Object))
      expect(mockWindow.location.href).not.toEqual('')
    })

    test('If form validation fails, don\'t save and don\'t go home', async () => {
      // Spy on form validation to make it fail
      jest.spyOn(wrapper.vm, 'validateCurrentForm')
      wrapper.vm.validateCurrentForm.mockImplementation(() => false)
      await flushPromises()

      wrapper.find('#go-home-button').trigger('click')
      await flushPromises()

      expect(wrapper.vm.validateCurrentForm).toHaveBeenCalled()
      expect(axios.post).not.toHaveBeenCalled()
      expect(mockWindow.location.href).toEqual('')
    })
    // Todo : test the navigation : back, next
  })
  // Todo : test the swapEditor flow
  // Todo : test the save button
})
