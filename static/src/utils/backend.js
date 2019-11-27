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
  'fichier-reponse': '/api/fichier-reponse/',
  question: '/api/question/',
  questionnaire: '/api/questionnaire/',
  theme: '/api/theme/',
  user: '/api/user/',
}

// From ecc/urls.py. 
// For the frontend queries we need to add leading slashes.
const viewUrls = {
    welcome: 'bienvenue/',
    // Questionnaire pages
    'questionnaire-detail': 'questionnaire/<int:pk>/',
    'questionnaire-create': 'questionnaire/controle-<int:pk>/creer',
    'questionnaire-edit': 'questionnaire/modifier/<int:pk>/',
    trash: 'questionnaire/corbeille/<int:pk>/',
    // Control pages
    'control-detail': 'accueil/#control-<int:pk>',
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

for (const [name, url] of Object.entries(viewUrls)) {
  urlMaker[name] = (id) => {
    if (!url.includes('<int:pk>')) {
      return '/' + url
    }
    if (id === undefined) {
      throw Error('Url ' + url + ' needs id arg')
    }
    return '/' + url.replace('<int:pk>', id)
  }
}

export default urlMaker
