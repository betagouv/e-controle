import { mount } from '@vue/test-utils'
import QuestionnaireBodyCreate from '../QuestionnaireBodyCreate.vue'

describe('QuestionnaireBodyCreate.vue', () => {
  test('is a Vue instance', () => {
    const wrapper = mount(QuestionnaireBodyCreate)
    expect(wrapper.isVueInstance()).toBeTruthy()
  })
})

