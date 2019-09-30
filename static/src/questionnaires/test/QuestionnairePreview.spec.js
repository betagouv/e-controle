import { mount, shallowMount } from "@vue/test-utils";

import PublishConfirmModal from '../PublishConfirmModal'
import QuestionnairePreview from '../QuestionnairePreview.vue'
import testUtils from '../../utils/testUtils'
import Wizard from '../../utils/Wizard'


describe('QuestionnairePreview.vue', () => {
  test('is a Vue instance', () => {
    // shallowMount stubs out all children
    const wrapper = shallowMount(QuestionnairePreview)
    expect(wrapper.isVueInstance()).toBeTruthy()
  })

  test('emits "back" when Wizard emits "previous"', () => {
    // Stub out Wizard. (Other child components are really instantiated)
    const wrapper = mount(QuestionnairePreview, {
      stubs: {
        Wizard: true
      }
    })

    const wizard = wrapper.find(Wizard).vm
    wizard.$emit('previous')

    testUtils.assertHasEmmitted(wrapper, 'back', 1)
  })

  test('emits "publish-questionnaire" when PublishConfirmModal emits "confirm"', () => {
    const wrapper = mount(QuestionnairePreview, {
      stubs: {
        PublishConfirmModal: true
      }
    })

    const modal = wrapper.find(PublishConfirmModal).vm
    modal.$emit('confirm')

    testUtils.assertHasEmmitted(wrapper, 'publish-questionnaire', 1)
  })

  test('emits "save-draft" when save button is clicked', () => {
    const wrapper = shallowMount(QuestionnairePreview)
    testUtils.assertNothingEmitted(wrapper)

    wrapper.find('#saveDraftFromPreviewButton').trigger('click')

    testUtils.assertHasEmmitted(wrapper, 'save-draft', 1)
  })

  test('shows modal with error when parent emits "publish-questionnaire-error"', () => {
    const wrapper = shallowMount(QuestionnairePreview)
    expect(wrapper.vm.$data.publishError).toBe(undefined)

    const errorMessage = 'oh noes'
    wrapper.vm.$parent.$emit('publish-questionnaire-error', { error: errorMessage })

    expect(wrapper.vm.$data.publishError.error).toBe(errorMessage)
  })

})