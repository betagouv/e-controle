import { mount, createLocalVue } from '@vue/test-utils'
import { getField, updateField } from 'vuex-map-fields'
import QuestionnaireMetadataCreate from '../QuestionnaireMetadataCreate.vue'
import Vuex from 'vuex'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('QuestionnaireMetadataCreate.vue', () => {
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
    const wrapper = mount(QuestionnaireMetadataCreate, { store, localVue })
    expect(wrapper.isVueInstance()).toBeTruthy()
  })
})
