import { shallowMount } from '@vue/test-utils'
import QuestionnaireCreate from '../QuestionnaireCreate.vue'

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
})

