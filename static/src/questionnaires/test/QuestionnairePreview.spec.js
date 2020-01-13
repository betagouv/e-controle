import { shallowMount, createLocalVue } from '@vue/test-utils'
import { getField, updateField } from 'vuex-map-fields'

import QuestionnairePreview from '../QuestionnairePreview.vue'
import QuestionnaireDetailForPreview from '../QuestionnaireDetailForPreview'
import Vuex from 'vuex'

// Create a localVue, which won't affect the global Vue constructor.
const localVue = createLocalVue()
localVue.use(Vuex)

describe('QuestionnairePreview.vue', () => {
  // Todo move this mock store to separate file for reuse
  let store
  const currentQuestionnaire = { id: 12345 }
  beforeEach(() => {
    store = new Vuex.Store({
      state: {
        currentQuestionnaire: currentQuestionnaire,
      },
      getters: {
        getField,
      },
      mutations: {
        updateField,
      },
    })
  })

  test('is a Vue instance', () => {
    // shallowMount stubs out all children
    const wrapper = shallowMount(QuestionnairePreview, { store, localVue })
    expect(wrapper.isVueInstance()).toBeTruthy()
  })

  test('passes questionnaire to QuestionnaireDetailForPreview', () => {
    const wrapper = shallowMount(QuestionnairePreview, {
      store,
      localVue,
      stubs: {
        QuestionnaireDetailForPreview: true,
      },
    })

    const child = wrapper.find(QuestionnaireDetailForPreview)
    expect(child.exists()).toBe(true)
    expect(child.props().questionnaire).toEqual(currentQuestionnaire)
  })

})
