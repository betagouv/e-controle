import { shallowMount, createLocalVue } from '@vue/test-utils'
import { getField, updateField } from 'vuex-map-fields'

import QuestionnairePreview from '../QuestionnairePreview.vue'
import Vuex from 'vuex'

// Create a localVue, which won't affect the global Vue constructor.
const localVue = createLocalVue()
localVue.use(Vuex)

describe('QuestionnairePreview.vue', () => {
  // Todo move this mock store to separate file for reuse
  let store
  beforeEach(() => {
    store = new Vuex.Store({
      state: {
        currentQuestionnaire: '',
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

})
