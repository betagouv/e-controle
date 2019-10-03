import axios from 'axios'
import { shallowMount } from '@vue/test-utils'
import flushPromises from 'flush-promises'
import QuestionnaireCreate from '../QuestionnaireCreate.vue'
import testUtils from '../../utils/testUtils'

jest.mock('axios')

describe('QuestionnaireCreate.vue', () => {

  beforeEach(() => {
    jest.resetModules();
    jest.clearAllMocks();
  });

  test('is a Vue instance', () => {
    const wrapper = shallowMount(
        QuestionnaireCreate,
        {
          propsData: {
            controlId: 1
          }
    })
    expect(wrapper.isVueInstance()).toBeTruthy()
  })

  ///////////
  // Setup //
  ///////////
  test('crashes without a controlId or questionnaireId', () => {
    expect(() => {
      shallowMount(QuestionnaireCreate)
    }).toThrow()
  })

  test('runs with controlId (create new questionnaire)', () => {
    expect(() => {
      shallowMount(QuestionnaireCreate, { propsData: { controlId: 1}})
    }).not.toThrow()
  })

  describe('Setup : update existing questionnaire', () => {
    test('sets up without crashing', () => {
      const questionnaireId = 1;
      axios.get.mockResolvedValue({ data: { id: questionnaireId }})

      expect(() => {
        shallowMount(QuestionnaireCreate, { propsData: { questionnaireId: questionnaireId}})
      }).not.toThrow()

    })

    test('gets questionnaire from server', () => {
      const questionnaire = { id: 4, is_draft: true };
      axios.get.mockResolvedValue({ data: questionnaire})

      const wrapper = shallowMount(QuestionnaireCreate, { propsData: { questionnaireId: questionnaire.id}})

      expect(axios.get).toBeCalledWith('/api/questionnaire/' + questionnaire.id);
    })

    test('stores questionnaire in frontend', async () => {
      const questionnaire = { id: 4, is_draft: true };
      axios.get.mockResolvedValue({ data: questionnaire})

      const wrapper = shallowMount(QuestionnaireCreate, { propsData: { questionnaireId: questionnaire.id}})
      await flushPromises()

      assert.deepEqual(wrapper.vm.questionnaire, questionnaire)
    })

    describe('displays error', () => {
      test('if cannot get questionnaire from server', async () => {
        const questionnaire = { id: 4, is_draft: false };
        // Error has weird unexpected format
        axios.get.mockRejectedValue({ stuff: 'things'})

        const wrapper = shallowMount(QuestionnaireCreate, { propsData: { questionnaireId: questionnaire.id}})
        assert(wrapper.vm.errorMessage === "")
        assert(!wrapper.vm.hasErrors)
        assert(!wrapper.find('#questionnaire-create-error').exists())

        await flushPromises()

        assert(wrapper.vm.errorMessage !== "")
        assert(wrapper.vm.hasErrors)
        assert(wrapper.find('#questionnaire-create-error').exists())
      })

      test('if questionnaire is not a draft', async () => {
        const questionnaire = { id: 4, is_draft: false };
        axios.get.mockResolvedValue({ data: questionnaire})

        const wrapper = shallowMount(QuestionnaireCreate, { propsData: { questionnaireId: questionnaire.id}})
        assert(wrapper.vm.errorMessage === "")
        assert(!wrapper.vm.hasErrors)
        assert(!wrapper.find('#questionnaire-create-error').exists())

        await flushPromises()

        assert(wrapper.vm.errorMessage !== "")
        assert(wrapper.vm.hasErrors)
        assert(wrapper.find('#questionnaire-create-error').exists())
      })
    })

    test('moves to first step of wizard', async () => {
      const questionnaire = { id: 4, is_draft: true };
      axios.get.mockResolvedValue({ data: questionnaire})

      const wrapper = shallowMount(QuestionnaireCreate, { propsData: { questionnaireId: questionnaire.id}})
      assert(!wrapper.find('#questionnaire-metadata-create').isVisible())
      await flushPromises()

      assert(wrapper.find('#questionnaire-metadata-create').isVisible())
    })

    test('passes questionnaire to first step of wizard', async () => {
    })

  })

  describe('Publishing flow', () => {
    test('shows wait modal when child emits publish-questionnaire', () => {
      const wrapper = shallowMount(QuestionnaireCreate, { propsData: { controlId: 1}})
      assert(!testUtils.isModalShowing(wrapper, '#savingModal'))
      assert(!testUtils.isModalShowing(wrapper, '#savedModal'))

      wrapper.vm.$refs.previewChild.$emit('publish-questionnaire')

      assert(testUtils.isModalShowing(wrapper, '#savingModal'))
      // Final modal not showing yet
      assert(!testUtils.isModalShowing(wrapper, '#savedModal'))
    })

    test('calls save api when child emits publish-questionnaire', () => {
      const controlId = 1
      const wrapper = shallowMount(QuestionnaireCreate, { propsData: { controlId: controlId}})

      wrapper.vm.$refs.previewChild.$emit('publish-questionnaire')

      // POST is called, because no questionnaire.id, so it's a creation.
      expect(axios.post).toBeCalledWith('/api/questionnaire/', { control: controlId, is_draft: false});
    })

    test('shows success modal when publish happened successfully', async () => {
      const controlId = 1
      const wrapper = shallowMount(QuestionnaireCreate, { propsData: { controlId: controlId}})
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
      const wrapper = shallowMount(QuestionnaireCreate, { propsData: { controlId: controlId}})
      // Save returns error
      const error = {error: 'I am not happpyyyy', details: [ 'stuff', 'more stuff' ]}
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
      testUtils.assertHasEmmitted(wrapper,'publish-questionnaire-error', 1)
      assert.deepEqual(wrapper.emitted()['publish-questionnaire-error'][0][0], error)
    })
  })

})

