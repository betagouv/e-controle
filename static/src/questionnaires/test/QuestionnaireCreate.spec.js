import { shallowMount, createLocalVue } from '@vue/test-utils'
import { getField, updateField } from 'vuex-map-fields'
import QuestionnaireCreate from '../QuestionnaireCreate.vue'
import Vuex from 'vuex'
import { loadStatuses } from '../../store'
import flushPromises from 'flush-promises'

jest.mock('axios')
const localVue = createLocalVue()
localVue.use(Vuex)

describe('QuestionnaireCreate.vue', () => {
  let store
  const currentQuestionnaire = { id: 12345 }

  beforeEach(() => {
    jest.resetModules()
    jest.clearAllMocks()

    store = new Vuex.Store({
      state: {
        currentQuestionnaire: currentQuestionnaire,
      },
      getters: {
        getField,
      },
      mutations: {
        updateField,
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

    test('moves to first State', async () => {
      const controlId = 1
      // Todo : this is the "full" state, prune the vars we don't need
      store = new Vuex.Store({
        state: {
          config: {},
          controls: [],
          controlsLoadStatus: loadStatuses.LOADING,
          currentQuestionnaire: {},
          editingControl: {},
          editingUser: {},
          editingProfileType: '',
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

      const wrapper = shallowMount(
        QuestionnaireCreate,
        {
          propsData: {
            controlId: 1,
          },
          store,
          localVue,
        })

      store.controls = [
        {
          id: controlId,
        },
      ]

      store.updateControlsLoadStatus = loadStatuses.SUCCESS

      await flushPromises() // todo is this needed?
      // Todo : the watcher func is not being run, it's not logging to console.
      // Maybe use store.commit?
      expect(wrapper.vm.state).toEqual(1)
    })

  })

/*
    test('moves to first step of wizard', async () => {
      const wrapper = shallowMount(
        QuestionnaireCreate,
        {
          propsData: {
            controlId: 1,
          },
          store,
          localVue,
        })

      assert(!wrapper.find('#questionnaire-metadata-create').isVisible())
      await flushPromises()

      assert(wrapper.find('#questionnaire-metadata-create').isVisible())
    })


      test('passes questionnaire to child components', async () => {
        const controlId = 6
        const wrapper = shallowMount(QuestionnaireCreate, { propsData: { controlId: controlId } })
        testUtils.assertHasEmmitted(wrapper, 'questionnaire-updated', 1)
        testUtils.assertLastEmit(wrapper, 'questionnaire-updated', { control: controlId })
      })
    })

    describe('update existing questionnaire', () => {
      test('sets up without crashing', () => {
        const questionnaireId = 1
        axios.get.mockResolvedValue({ data: { id: questionnaireId } })

        expect(() => {
          shallowMount(QuestionnaireCreate, { propsData: { questionnaireId: questionnaireId } })
        }).not.toThrow()
      })

      test('gets questionnaire from server', () => {
        const questionnaire = { id: 4, is_draft: true }
        axios.get.mockResolvedValue({ data: questionnaire })

        const wrapper = shallowMount(QuestionnaireCreate, { propsData: { questionnaireId: questionnaire.id } })

        expect(axios.get).toBeCalledWith('/api/questionnaire/' + questionnaire.id)
      })

      test('stores questionnaire in frontend', async () => {
        const questionnaire = { id: 4, is_draft: true }
        axios.get.mockResolvedValue({ data: questionnaire })

        const wrapper = shallowMount(QuestionnaireCreate, { propsData: { questionnaireId: questionnaire.id } })
        await flushPromises()

        assert.deepEqual(wrapper.vm.questionnaire, questionnaire)
      })

      describe('displays error', () => {
        test('if cannot get questionnaire from server', async () => {
          const questionnaire = { id: 4, is_draft: false }
          // Error has weird unexpected format
          axios.get.mockRejectedValue({ stuff: 'things' })

          const wrapper = shallowMount(QuestionnaireCreate, { propsData: { questionnaireId: questionnaire.id } })
          assert(wrapper.vm.errorMessage === '')
          assert(!wrapper.vm.hasErrors)
          assert(!wrapper.find('#questionnaire-create-error').exists())

          await flushPromises()

          assert(wrapper.vm.errorMessage !== '')
          assert(wrapper.vm.hasErrors)
          assert(wrapper.find('#questionnaire-create-error').exists())
        })

        test('if questionnaire is not a draft', async () => {
          const questionnaire = { id: 4, is_draft: false }
          axios.get.mockResolvedValue({ data: questionnaire })

          const wrapper = shallowMount(QuestionnaireCreate, { propsData: { questionnaireId: questionnaire.id } })
          assert(wrapper.vm.errorMessage === '')
          assert(!wrapper.vm.hasErrors)
          assert(!wrapper.find('#questionnaire-create-error').exists())

          await flushPromises()

          assert(wrapper.vm.errorMessage !== '')
          assert(wrapper.vm.hasErrors)
          assert(wrapper.find('#questionnaire-create-error').exists())
        })
      })

      test('moves to first step of wizard', async () => {
        const questionnaire = { id: 4, is_draft: true }
        axios.get.mockResolvedValue({ data: questionnaire })

        const wrapper = shallowMount(QuestionnaireCreate, { propsData: { questionnaireId: questionnaire.id } })
        assert(!wrapper.find('#questionnaire-metadata-create').isVisible())
        await flushPromises()

        assert(wrapper.find('#questionnaire-metadata-create').isVisible())
      })

      test('passes questionnaire to child components', async () => {
        const questionnaire = { id: 4, is_draft: true }
        axios.get.mockResolvedValue({ data: questionnaire })

        const wrapper = shallowMount(QuestionnaireCreate, { propsData: { questionnaireId: questionnaire.id } })
        testUtils.assertNotEmitted(wrapper, 'questionnaire-updated')
        await flushPromises()

        testUtils.assertHasEmmitted(wrapper, 'questionnaire-updated', 1)
        testUtils.assertLastEmit(wrapper, 'questionnaire-updated', questionnaire)
      })
    })
  })

  describe('Publishing flow', () => {
    test('shows wait modal when child emits publish-questionnaire', () => {
      const wrapper = shallowMount(QuestionnaireCreate, { propsData: { controlId: 1 } })
      assert(!testUtils.isModalShowing(wrapper, '#savingModal'))
      assert(!testUtils.isModalShowing(wrapper, '#savedModal'))

      wrapper.vm.$refs.previewChild.$emit('publish-questionnaire')

      assert(testUtils.isModalShowing(wrapper, '#savingModal'))
      // Final modal not showing yet
      assert(!testUtils.isModalShowing(wrapper, '#savedModal'))
    })

    test('calls save api when child emits publish-questionnaire', () => {
      const controlId = 1
      const wrapper = shallowMount(QuestionnaireCreate, { propsData: { controlId: controlId } })

      wrapper.vm.$refs.previewChild.$emit('publish-questionnaire')

      // POST is called, because no questionnaire.id, so it's a creation.
      expect(axios.post).toBeCalledWith('/api/questionnaire/', { control: controlId, is_draft: false })
    })

    test('shows success modal when publish happened successfully', async () => {
      const controlId = 1
      const wrapper = shallowMount(QuestionnaireCreate, { propsData: { controlId: controlId } })
      assert(!testUtils.isModalShowing(wrapper, '#savingModal'))
      assert(!testUtils.isModalShowing(wrapper, '#savedModal'))

      // Mock out wait function to resolve immediately without wait.
      wrapper.vm.wait = () => Promise.resolve()
      axios.post.mockResolvedValue({})

      wrapper.vm.$refs.previewChild.$emit('publish-questionnaire')

      // Resolve all promises
      await flushPromises()

      // Intermediate modal is gone
      assert(!testUtils.isModalShowing(wrapper, '#savingModal'))
      assert(testUtils.isModalShowing(wrapper, '#savedModal'))
    })

    test('signals back to child when publish returned errors', async () => {
      const controlId = 1
      const wrapper = shallowMount(QuestionnaireCreate, { propsData: { controlId: controlId } })
      // Save returns error
      const error = { error: 'I am not happpyyyy', details: ['stuff', 'more stuff'] }
      axios.post.mockRejectedValue(error)
      testUtils.assertNotEmitted(wrapper, 'publish-questionnaire-error')

      wrapper.vm.$refs.previewChild.$emit('publish-questionnaire')
      // Resolve all promises
      await flushPromises()

      // Intermediate modal is gone
      assert(!testUtils.isModalShowing(wrapper, '#savingModal'))
      // Success modal not displayed
      assert(!testUtils.isModalShowing(wrapper, '#savedModal'))

      // Event sent for child
      testUtils.assertHasEmmitted(wrapper, 'publish-questionnaire-error', 1)
      assert.deepEqual(wrapper.emitted()['publish-questionnaire-error'][0][0], error)
    })
  })
  */
})
