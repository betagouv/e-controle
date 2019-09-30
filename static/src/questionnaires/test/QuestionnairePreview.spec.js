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

  const wait = (time_millis) => {
    return new Promise((resolve) => {
      let id = setTimeout(() => {
        clearTimeout(id);
        resolve()
      }, time_millis)
    })
  }

  const waitNT = ctx => new Promise(resolve => ctx.$nextTick(resolve))
  const waitRAF = () => new Promise(resolve => requestAnimationFrame(resolve))

  // Publish questionnaire flow
  test('shows PublishConfirmModal when button is clicked', async () => {
    const wrapper = mount(
        QuestionnairePreview,
        {
          stubs: {
            transition: false
          }
        })
    console.log(wrapper.find('#publishConfirmModal').html())
    assert(!testUtils.isModalShowing(wrapper, '#publishConfirmModal'))

    wrapper.find('#publishButton').trigger('click')
    await wait(4000)
    await waitNT(wrapper.vm)
    await waitRAF()
    await waitNT(wrapper.vm)
    await waitRAF()

    console.log(wrapper.find('#publishConfirmModal').html())
    assert(testUtils.isModalShowing(wrapper, '#publishConfirmModal'))
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