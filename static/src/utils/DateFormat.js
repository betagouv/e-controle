const DISPLAY_FORMAT = { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' }
const LOCALE = 'fr-FR'

export default function (value) {
  if (value) {
    const date = new Date(value)
    return date.toLocaleDateString(LOCALE, DISPLAY_FORMAT)
  }
}

export const toBackendFormat = (value) => {
  if (value) {
    const date = new Date(value)
    const day = date.getDate()
    const month = date.getMonth() + 1
    const year = date.getFullYear()
    return `${year}-${month}-${day}`
  }
}
