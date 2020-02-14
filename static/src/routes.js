import QuestionnaireBodyCreate from './questionnaires/QuestionnaireBodyCreate'
import QuestionnaireMetadataCreate from './questionnaires/QuestionnaireMetadataCreate'
import QuestionnairePreview from './questionnaires/QuestionnairePreview'

const routes = [
  {
    path: '/',
    redirect: { name: 'questionnaire-metadata-create' },
  },
  {
    name: 'questionnaire-metadata-create',
    path: '/questionnaire/modifier/:questionnaireId/#1-intro',
    component: QuestionnaireMetadataCreate,
  },
  {
    name: 'questionnaire-body-create',
    path: '/questionnaire/modifier/:questionnaireId/#2-questions',
    component: QuestionnaireBodyCreate,
  },
  {
    name: 'questionnaire-preview',
    path: '/questionnaire/modifier/:questionnaireId/#3-apercu',
    component: QuestionnairePreview,
  },
]

export default routes
