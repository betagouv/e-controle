import { mount, shallowMount, TransitionStub } from "@vue/test-utils";

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

  test('updates its questionnaire when parent emits questionnaire-updated', () => {
    const wrapper = shallowMount(QuestionnairePreview)
    const questionnaire = {
      id: 7,
      title: 'Bibimbaps',
      is_draft: true,
      themes: [
          {
            id: 234,
            questionnaire: 7,
            title: 'good theme man',
          },
      ]
    }
    assert.deepEqual(wrapper.vm.questionnaire, {})

    wrapper.vm.$parent.$emit('questionnaire-updated', questionnaire)

    assert.deepEqual(wrapper.vm.questionnaire, questionnaire)
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

  // Publish questionnaire flow
  test('shows PublishConfirmModal when button is clicked', async () => {
    const wrapper = shallowMount(QuestionnairePreview)
    assert(!testUtils.isModalShowing(wrapper, '#publishConfirmModal'))

    wrapper.find('#publishButton').trigger('click')

    assert(testUtils.isModalShowing(wrapper, '#publishConfirmModal'))
  })

  test('emits "publish-questionnaire" when PublishConfirmModal emits "confirm"', () => {
    const wrapper = mount(QuestionnairePreview, {
      stubs: {
        PublishConfirmModal: true
      }
    })
    testUtils.assertNothingEmitted(wrapper)

    const modal = wrapper.find(PublishConfirmModal).vm
    modal.$emit('confirm')

    testUtils.assertHasEmmitted(wrapper, 'publish-questionnaire', 1)
  })

  // Save draft flow
  test('emits "save-draft" when save button is clicked', () => {
    const wrapper = shallowMount(QuestionnairePreview)
    testUtils.assertNothingEmitted(wrapper)

    wrapper.find('#saveDraftFromPreviewButton').trigger('click')

    testUtils.assertHasEmmitted(wrapper, 'save-draft', 1)
  })

  // Publish questionnaire error flow
  test('shows modal when parent emits "publish-questionnaire-error"', () => {
    const wrapper = shallowMount(QuestionnairePreview)
    assert(!testUtils.isModalShowing(wrapper, '#publishConfirmModal'))

    const errorMessage = 'oh noes'
    wrapper.vm.$parent.$emit('publish-questionnaire-error', { error: errorMessage })

    assert(testUtils.isModalShowing(wrapper, '#publishConfirmModal'))
  })

  test('stores error when parent emits "publish-questionnaire-error"', () => {
    const wrapper = shallowMount(QuestionnairePreview)
    assert(!wrapper.vm.$data.publishError)

    const errorMessage = 'oh noes'
    wrapper.vm.$parent.$emit('publish-questionnaire-error', { error: errorMessage })

    assert.strictEqual(wrapper.vm.$data.publishError.error, errorMessage)
  })
})