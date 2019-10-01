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

  test('runs with questionnaireId (update existing questionnaire)', () => {
    const questionnaireId = 1;
    axios.get.mockResolvedValue({ data: { id: questionnaireId }})

    expect(() => {
      shallowMount(QuestionnaireCreate, { propsData: { questionnaireId: questionnaireId}})
    }).not.toThrow()

    // Called axios to load questionnaire
    expect(axios.get).toBeCalledWith('/api/questionnaire/' + questionnaireId);
  })

  test('shows wait modal when child emits publish-questionnaire', () => {
    const wrapper = shallowMount(QuestionnaireCreate, { propsData: { controlId: 1}})
    assert(!testUtils.isModalShowing(wrapper, '#savingModal'))

    wrapper.vm.$refs.previewChild.$emit('publish-questionnaire')

    assert(testUtils.isModalShowing(wrapper, '#savingModal'))
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

    // Mock out wait function to resolve immediately without wait.
    wrapper.vm.wait = () => Promise.resolve()
    axios.post.mockResolvedValue({})

    wrapper.vm.$refs.previewChild.$emit('publish-questionnaire')

    // Resolve all promises
    await flushPromises()

    assert(!testUtils.isModalShowing(wrapper, '#savingModal'))
    assert(testUtils.isModalShowing(wrapper, '#savedModal'))
  })

})

