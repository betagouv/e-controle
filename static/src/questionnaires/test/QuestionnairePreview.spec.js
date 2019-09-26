import { mount, shallowMount } from "@vue/test-utils";

import PublishConfirmModal from '../PublishConfirmModal'
import QuestionnairePreview from '../QuestionnairePreview.vue'
import Wizard from '../../utils/Wizard'

const assertHasEmmitted = (obj, eventName, numTimes) => {
  expect(obj.emitted()).toHaveProperty(eventName)
  expect(obj.emitted()[eventName].length).toEqual(numTimes)
}

describe('QuestionnairePreview.vue', () => {
  test('is a Vue instance', () => {
    // shallowMount stubs out all children
    const wrapper = shallowMount(QuestionnairePreview)
    expect(wrapper.isVueInstance()).toBeTruthy()
  })

  test('emits "back" when Wizard emits "previous"', () => {
    // Stub out a Wizard. (Other child components are really instantiated)
    const wrapper = mount(QuestionnairePreview, {
      stubs: {
        Wizard: true
      }
    })

    const wizard = wrapper.find(Wizard).vm
    wizard.$emit('previous')

    assertHasEmmitted(wrapper, 'back', 1)
  })

  test('emits "publish-questionnaire" when PublishConfirmModal emits "confirm"', () => {
    // Stub out a Wizard. (Other child components are really instantiated)
    const wrapper = mount(QuestionnairePreview, {
      stubs: {
        PublishConfirmModal: true
      }
    })

    const wizard = wrapper.find(PublishConfirmModal).vm
    wizard.$emit('confirm')

    assertHasEmmitted(wrapper, 'publish-questionnaire', 1)
  })
})