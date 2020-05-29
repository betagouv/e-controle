const LOCALE = 'fr-FR'
const OPTIONS = { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' }

export default function (value) {
  if (value) {
    const date = new Date(value)
    return date.toLocaleDateString(LOCALE, OPTIONS)
  }
}
