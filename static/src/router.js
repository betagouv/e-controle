import QuestionnaireBodyCreate from './questionnaires/QuestionnaireBodyCreate'
import QuestionnaireMetadataCreate from './questionnaires/QuestionnaireMetadataCreate'
import QuestionnairePreview from './questionnaires/QuestionnairePreview'
import VueRouter from 'vue-router'

const routes = [
  {
    path: '/',
    redirect: { name: 'questionnaire-metadata-create' },
  },
  {
    name: 'questionnaire-metadata-create',
    path: '/1-introduction',
    component: QuestionnaireMetadataCreate,
    meta: { stepNumber: 1 },
  },
  {
    name: 'questionnaire-body-create',
    path: '/2-questions',
    component: QuestionnaireBodyCreate,
    meta: { stepNumber: 2 },
  },
  {
    name: 'questionnaire-preview',
    path: '/3-apercu',
    component: QuestionnairePreview,
    meta: { stepNumber: 3 },
  },
]

const router = new VueRouter({
  routes,
})

export default router
