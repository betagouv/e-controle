import { mount, createLocalVue, shallowMount } from '@vue/test-utils'
import { getField, updateField } from 'vuex-map-fields'

import QuestionnaireBodyCreate from '../QuestionnaireBodyCreate.vue'
import Vuex from 'vuex'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('QuestionnaireBodyCreate.vue', () => {
  let store
  let themes
  beforeEach(() => {
    themes = [
      {
        id: 777,
        questions: [
          {
            id: 111,
            order: 0,
          },
          {
            id: 222,
            order: 1,
          },
        ],
      },
    ]
    store = new Vuex.Store({
      state: {
        currentQuestionnaire: { themes: themes },
      },
      getters: {
        getField,
      },
      mutations: {
        updateField,
      },
    })
  })

  afterEach(() => {
    // If we removed error output in previous test, set it back for next test.
    if (console.error.mockRestore) {
      console.error.mockRestore()
    }
  })

  test('is a Vue instance', () => {
    const wrapper = mount(QuestionnaireBodyCreate, { store, localVue })
    expect(wrapper.isVueInstance()).toBeTruthy()
    expect(wrapper.vm.themes).toEqual(themes)
  })

  describe('Swapping questions', () => {
    let wrapper
    beforeEach(() => {
      wrapper = shallowMount(
        QuestionnaireBodyCreate,
        { store, localVue },
      )
    })
    test('moving question down changes question order', async () => {
      const question0 = themes[0].questions[0]
      const question1 = themes[0].questions[1]

      wrapper.find('#theme-0-question-0 .move-down-button').trigger('click')

      // Questions are swapped in array
      expect(wrapper.vm.themes[0].questions[0].id).toEqual(question1.id)
      expect(wrapper.vm.themes[0].questions[1].id).toEqual(question0.id)
      // Order field is updated to reflect new position
      expect(wrapper.vm.themes[0].questions[0].order).toEqual(0)
      expect(wrapper.vm.themes[0].questions[1].order).toEqual(1)
    })

    test('moving question up changes question order', async () => {
      const question0 = themes[0].questions[0]
      const question1 = themes[0].questions[1]

      wrapper.find('#theme-0-question-1 .move-up-button').trigger('click')

      // Questions are swapped in array
      expect(wrapper.vm.themes[0].questions[0].id).toEqual(question1.id)
      expect(wrapper.vm.themes[0].questions[1].id).toEqual(question0.id)
      // Order field is updated to reflect new position
      expect(wrapper.vm.themes[0].questions[0].order).toEqual(0)
      expect(wrapper.vm.themes[0].questions[1].order).toEqual(1)
    })

    test('cannot move first question up', async () => {
      // Disable error logging since we expect it in this test
      jest.spyOn(console, 'error')
      console.error.mockImplementation(() => {})

      const question0 = themes[0].questions[0]
      const question1 = themes[0].questions[1]

      // Button is disabled
      expect(wrapper.find('#theme-0-question-0 .move-up-button').classes()).toContain('disabled')

      // Click anyway
      wrapper.find('#theme-0-question-0 .move-up-button').trigger('click')

      // Questions are NOT swapped in array
      expect(wrapper.vm.themes[0].questions[0].id).toEqual(question0.id)
      expect(wrapper.vm.themes[0].questions[1].id).toEqual(question1.id)
      // Order field is unchanged
      expect(wrapper.vm.themes[0].questions[0].order).toEqual(0)
      expect(wrapper.vm.themes[0].questions[1].order).toEqual(1)
    })

    test('cannot move last question down', async () => {
      // Disable error logging since we expect it in this test
      jest.spyOn(console, 'error')
      console.error.mockImplementation(() => {})

      const question0 = themes[0].questions[0]
      const question1 = themes[0].questions[1]

      // Button is disabled
      expect(wrapper.find('#theme-0-question-1 .move-down-button').classes()).toContain('disabled')

      // Click anyway
      wrapper.find('#theme-0-question-1 .move-down-button').trigger('click')

      // Questions are NOT swapped in array
      expect(wrapper.vm.themes[0].questions[0].id).toEqual(question0.id)
      expect(wrapper.vm.themes[0].questions[1].id).toEqual(question1.id)
      // Order field is unchanged
      expect(wrapper.vm.themes[0].questions[0].order).toEqual(0)
      expect(wrapper.vm.themes[0].questions[1].order).toEqual(1)
    })
  })
})
