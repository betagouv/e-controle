import { shallowMount } from '@vue/test-utils'
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
          activeStepNumber: 2,
          stepTitles: ['Step the first', 'Step the second', 'Step the third', 'Step the last'],
        },
      })
    expect(wrapper.isVueInstance()).toBeTruthy()
  })

  test('displays the steps', () => {
    const wrapper = shallowMount(
      Wizard,
      {
        propsData: {
          activeStepNumber: 2,
          stepTitles: ['Step the first', 'Step the last'],
        },
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
          activeStepNumber: 2,
          stepTitles: ['Step the first', 'Step the last'],
        },
      })

    expect(getStep(wrapper, 2).classes()).toContain('active')
    expect(getStep(wrapper, 1).classes()).not.toContain('active')
  })

  test('displays the done steps', () => {
    const wrapper = shallowMount(
      Wizard,
      {
        propsData: {
          activeStepNumber: 2,
          stepTitles: ['Step the first', 'Step the second', 'Step the last'],
        },
      })

    expect(getStep(wrapper, 1).classes()).toContain('done')
    expect(getStep(wrapper, 2).classes()).not.toContain('done')
    expect(getStep(wrapper, 3).classes()).not.toContain('done')
  })

  test('emits next and previous', () => {
    const runEmitTest = (activeStepNumber, clickedStepNumber, emittedEventName) => {
      const wrapper = shallowMount(
        Wizard,
        {
          propsData: {
            activeStepNumber: activeStepNumber,
            stepTitles: ['Step the first', 'Step the second', 'Step the last'],
          },
        })
      testUtils.assertNothingEmitted(wrapper)

      getStep(wrapper, clickedStepNumber).vm.$emit('clickedStep')

      const emittedEvents = wrapper.emitted()
      expect(emittedEvents).toHaveProperty(emittedEventName)
      expect(emittedEvents[emittedEventName].length).toEqual(1)
      const emittedEventPayload = emittedEvents[emittedEventName][0]
      expect(emittedEventPayload[0]).toEqual(clickedStepNumber)
    }

    const runNoEmitTest = (activeStepNumber, clickedStepNumber) => {
      const wrapper = shallowMount(
        Wizard,
        {
          propsData: {
            activeStepNumber: activeStepNumber,
            stepTitles: ['Step the first', 'Step the second', 'Step the last'],
          },
        })
      testUtils.assertNothingEmitted(wrapper)

      getStep(wrapper, clickedStepNumber).vm.$emit('clickedStep')

      testUtils.assertNothingEmitted(wrapper)
    }

    // If you click the active step, nothing happens.
    runNoEmitTest(1, 1)
    runNoEmitTest(2, 2)
    runNoEmitTest(3, 3)

    // If you click the next step, 'next' event is emitted
    runEmitTest(1, 2, 'next')
    runEmitTest(2, 3, 'next')

    // If you click several steps forward, nothing happens (you can't skip steps forward)
    runNoEmitTest(1, 3)

    // If you click the previous step, 'previous' event is emitted
    runEmitTest(2, 1, 'previous')
    runEmitTest(3, 2, 'previous')
    // If you click several steps backwards, 'previous' event is emitted
    runEmitTest(3, 1, 'previous')
  })

})
