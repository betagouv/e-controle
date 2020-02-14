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
    path: '/1-intro',
    component: QuestionnaireMetadataCreate,
  },
  {
    name: 'questionnaire-body-create',
    path: '/2-questions',
    component: QuestionnaireBodyCreate,
  },
  {
    name: 'questionnaire-preview',
    path: '/3-apercu',
    component: QuestionnairePreview,
  },
]

const router = new VueRouter({
  routes,
})

export default router
