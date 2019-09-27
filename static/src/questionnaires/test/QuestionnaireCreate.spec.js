import axios from 'axios'
import { shallowMount } from '@vue/test-utils'
import QuestionnaireCreate from '../QuestionnaireCreate.vue'
import QuestionnaireMetadataCreate from '../QuestionnaireMetadataCreate'

jest.mock('axios', () => ({
  post: jest.fn(() => Promise.resolve({ data: 'saved-questionnaire' })),
  get: jest.fn(() => Promise.resolve({ data: 'saved-questionnaire' })),
  defaults: {},
}))

describe('QuestionnaireCreate.vue', () => {
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

  test('runs with controlId', () => {
    expect(() => {
      shallowMount(QuestionnaireCreate, { propsData: { controlId: 1}})
    }).not.toThrow()
  })

  test('runs with questionnaireId', () => {
    expect(() => {
      shallowMount(QuestionnaireCreate, { propsData: { questionnaireId: 1}})
    }).not.toThrow()
  })
})

