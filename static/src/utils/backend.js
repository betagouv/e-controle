/*
Usage :

For api :
backend.control() ---> '/api/control/'
backend.control(3) ---> '/api/control/3/'

For views :
backend['questionnaire-edit'](4) ---> 'questionnaire/modifier/4/'
*/

// Todo : make query to /api/ to get this
const apiUrls = {
  annexe: '/api/annexe/',
  control: '/api/control/',
  question: '/api/question/',
  questionnaire: '/api/questionnaire/',
  theme: '/api/theme/',
  user: '/api/user/',
  config: '/api/config',
}

// From ecc/urls.py.
// For the frontend queries we need to add leading slashes.
const backendViewUrls = {
  home: 'accueil/',
  welcome: 'bienvenue/',
  faq: 'faq/',
  upload: 'upload/',
  // Questionnaire pages
  'questionnaire-detail': 'questionnaire/<int:pk>/',
  'questionnaire-create': 'questionnaire/controle-<int:pk>/creer',
  'questionnaire-edit': 'questionnaire/modifier/<int:pk>/',
  'questionnaire-export': 'fichier-questionnaire/<int:pk>/',
  trash: 'questionnaire/corbeille/<int:pk>/',
  // Control pages
  'control-detail': 'accueil/#control-<int:pk>',
}
const viewUrls = {}
for (const [name, url] of Object.entries(backendViewUrls)) {
  viewUrls[name] = '/' + url
}

const urlMaker = {}

for (const [name, url] of Object.entries(apiUrls)) {
  urlMaker[name] = (id) => {
    if (id) {
      return url + id + '/'
    }
    return url
  }
}

urlMaker.currentUser = () => '/api/user/current/'
urlMaker.getUsersInControl = (controlId) => '/api/control/' + controlId + '/users/'
urlMaker.removeUserFromControl = (id) => '/api/user/' + id + '/remove-control/'
urlMaker.swapEditor = (questionnaireId) =>
  '/api/questionnaire/' + questionnaireId + '/changer-redacteur/'
urlMaker.deleteControl = (controlId) => '/api/deletion/' + controlId + '/delete-control/'
urlMaker.responseFileTrash = (responseFileId) =>
  '/api/fichier-reponse/corbeille/' + responseFileId + '/'

for (const [name, url] of Object.entries(viewUrls)) {
  urlMaker[name] = (id) => {
    if (!url.includes('<int:pk>')) {
      return url
    }
    if (id === undefined) {
      throw Error('Url ' + url + ' needs id arg')
    }
    return url.replace('<int:pk>', id)
  }
}

urlMaker.getIdFromViewUrl = (urlValue, urlName) => {
  if (viewUrls[urlName] === undefined) {
    return null
  }
  const regex = new RegExp('^' + viewUrls[urlName].replace('<int:pk>', '([0-9]+)') + '$')
  const found = urlValue.match(regex)
  if (!found) {
    return null
  }
  return parseInt(found[1], 10)
}

export default urlMaker
