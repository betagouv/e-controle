import axios from 'axios'
import { shallowMount } from '@vue/test-utils'
import QuestionnaireCreate from '../QuestionnaireCreate.vue'
import testUtils from '../../utils/testUtils'

jest.mock('axios')/*, () => ({
  post: jest.fn(() => Promise.resolve({ data: 'saved-questionnaire' })),
  get: jest.fn(() => Promise.resolve({ data: 'saved-questionnaire' })),
  defaults: {},
}))*/

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

  const wait = (time_millis) => {
    return new Promise((resolve) => {
      let id = setTimeout(() => {
        clearTimeout(id);
        resolve()
      }, time_millis)
    })
  }

  test('shows success modal when publish happened successfully', async () => {
    const controlId = 1
    const wrapper = shallowMount(QuestionnaireCreate, { propsData: { controlId: controlId}})
    axios.post.mockResolvedValue({})

    wrapper.vm.$refs.previewChild.$emit('publish-questionnaire')

    await wait(4000)

    assert(!testUtils.isModalShowing(wrapper, '#savingModal'))
    assert(testUtils.isModalShowing(wrapper, '#savedModal'))
  })

})

