import {mount} from "@vue/test-utils";
import QuestionnairePreview from '../QuestionnairePreview.vue'

describe('QuestionnairePreview.vue', () => {
  test('is a Vue instance', () => {
    const wrapper = mount(QuestionnairePreview)
    expect(wrapper.isVueInstance()).toBeTruthy()
  })
})