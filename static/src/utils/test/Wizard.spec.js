import { shallowMount } from "@vue/test-utils";
import testUtils from '../../utils/testUtils'
import Wizard from '../Wizard'

describe('Wizard.vue', () => {
  const getStep = (wrapper, stepNumber) => {
    return wrapper.find('[number="' + stepNumber + '"]')
  }

  test('is a Vue instance', () => {
    const wrapper = shallowMount(
        Wizard,
        {
          propsData: {
            activeStepNumber : 2,
            stepTitles : [ 'Step the first', 'Step the second', 'Step the third', 'Step the last' ]
          }
    })
    expect(wrapper.isVueInstance()).toBeTruthy()
  })

  test('displays the steps', () => {
    const wrapper = shallowMount(
        Wizard,
        {
          propsData: {
            activeStepNumber : 2,
            stepTitles : [ 'Step the first', 'Step the last' ]
          }
    })

    assert.equal(wrapper.findAll('[number]').length, 2)
    assert.equal(getStep(wrapper, 1).text(), 'Step the first')
    assert.equal(getStep(wrapper, 2).text(), 'Step the last')
  })

  test('displays the active step', () => {
    const wrapper = shallowMount(
        Wizard,
        {
          propsData: {
            activeStepNumber : 2,
            stepTitles : [ 'Step the first', 'Step the last' ]
          }
    })

    expect(getStep(wrapper, 2).classes()).toContain('active')
    expect(getStep(wrapper, 1).classes()).not.toContain('active')
  })

  test('displays the done steps', () => {
    const wrapper = shallowMount(
        Wizard,
        {
          propsData: {
            activeStepNumber : 2,
            stepTitles : [ 'Step the first', 'Step the second', 'Step the last' ]
          }
    })

    expect(getStep(wrapper, 1).classes()).toContain('done')
    expect(getStep(wrapper, 2).classes()).not.toContain('done')
    expect(getStep(wrapper, 3).classes()).not.toContain('done')
  })

  test('emits next and previous', () => {
    const runEmitTest = (activeStepNumber, clickedStepNumber, emittedEvent) => {
      const wrapper = shallowMount(
          Wizard,
          {
            propsData: {
              activeStepNumber : activeStepNumber,
              stepTitles : [ 'Step the first', 'Step the second', 'Step the last' ]
            }
      })
      testUtils.assertNothingEmitted(wrapper)

      getStep(wrapper, clickedStepNumber).vm.$emit('clickedStep')

      testUtils.assertHasEmmitted(wrapper, emittedEvent, 1)
    }

    const runNoEmitTest = (activeStepNumber, clickedStepNumber) => {
      const wrapper = shallowMount(
          Wizard,
          {
            propsData: {
              activeStepNumber : activeStepNumber,
              stepTitles : [ 'Step the first', 'Step the second', 'Step the last' ]
            }
      })
      testUtils.assertNothingEmitted(wrapper)

      getStep(wrapper, clickedStepNumber).vm.$emit('clickedStep')

      testUtils.assertNothingEmitted(wrapper)
    }

    runNoEmitTest(1, 1)
    runEmitTest(1, 2, 'next')
    runNoEmitTest(1, 3)

    runEmitTest(2, 1, 'previous')
    runNoEmitTest(2, 2)
    runEmitTest(2, 3, 'next')

    runNoEmitTest(3, 1)
    runEmitTest(3, 2, 'previous')
    runNoEmitTest(3, 3)
  })

})