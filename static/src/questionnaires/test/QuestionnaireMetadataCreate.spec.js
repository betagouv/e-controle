import {mount} from "@vue/test-utils";
import QuestionnaireMetadataCreate from '../QuestionnaireMetadataCreate.vue'

describe('QuestionnaireMetadataCreate.vue', () => {
  test('is a Vue instance', () => {
    const wrapper = mount(QuestionnaireMetadataCreate)
    expect(wrapper.isVueInstance()).toBeTruthy()
  })
})