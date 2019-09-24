

export const clearCache = function() {
  // Change the url (by adding a random querystring value) to force reload on next visit, because the
  // questionnaire data has changed. (it doesn't actually change the browser cache for the current url)
  history.pushState({}, "", "?reload=" + Math.random())
}
