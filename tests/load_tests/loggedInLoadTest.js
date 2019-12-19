import encoding from 'k6/encoding'
import http from 'k6/http'
import { check, group, sleep } from 'k6'
import { Counter, Trend } from 'k6/metrics'

export const options = {
  vus: 1,
  duration: '30s',
  throw: true,
}

// Example metrics
const myCounter = new Counter('my_counter')
const myTrend = new Trend('my_trend')

const testId = Math.floor(Math.random() * 1000)

const username = 'admin'
const password = 'faleco2019'

const loginUrl = 'http://127.0.0.1:8080/nonocat/login/'

export function setup() {
  // Get the csrf token : load the login form.
  const res = http.get(
    loginUrl,
    {
      headers: {
        Authorization: 'Basic ' + encoding.b64encode(`${username}:${password}`),
        Referer: loginUrl,
      },
    },
  )
  if (res.error || res.error_code) {
    throw Error(res.error_code + ' - ' + JSON.stringify(res.error))
  }

  // Get the csrf cookie from the form by grepping the page body.
  const found = res.body.match(/name="csrfmiddlewaretoken" value="(.*)"/)
  const csrf = found[1]
  console.log('using csrf', csrf)

  console.log('csrftoken cookie', res.cookies.csrftoken[0].value)
  const jar = http.cookieJar()
  jar.set('http://127.0.0.1:8080/nonocat/', 'csrftoken', res.cookies.csrftoken[0].value)

  // Log in
  const res2 = http.post(
    loginUrl,
    {
      csrfmiddlewaretoken: csrf,
      username: username,
      password: password,
    },
    {
      headers: {
        Referer: loginUrl,
      },
    },
  )
  console.log('res after login', JSON.stringify(res2))
  console.log('authenticated', JSON.stringify(res2.authenticated))
  if (res2.error || res2.error_code) {
    throw Error(res2.error_code + ' - ' + JSON.stringify(res2.error))
  }

  return { csrf: csrf }
}

const test = (url, csrf) => {
  // Start with the sleep so that you are sure it is run, even if the rest of the test crashes.
  // (to avoid DDOSing our own server!)
  sleep(1 + Math.random())

  try {
    const res = http.get(
      url,
      {
        headers: {
          Authorization: 'Basic ' + encoding.b64encode(`${username}:${password}`),
          Referer: loginUrl,
          'X-CSRF-Token': csrf,
        },
      },
    )

    if (res.error || res.error_code) {
      console.error('error', res.error_code, res.error)
      myCounter.add(1, { testId: testId, url: url, error: res.error, error_code: res.error_code })
    }

    console.log('Wanted', url, 'got redirected to', res.url)
    check(res, {
      'is status 200': (r) => r.status === 200,
      'no redirect': (r) => r.url === url,
    })

    console.log('res', res)
    console.log('cookies', JSON.stringify(res.cookies))
    console.log('csrftoken', res.cookies.csrftoken[0], JSON.stringify(res.cookies.csrftoken[0]))
    console.log('csrftoken name', res.cookies.csrftoken[0].name)
    console.log('csrftoken value', res.cookies.csrftoken[0].value)
    console.log('res.json()', res.json()) // crashes when non-authed. (when authed as well?)
    check(res, {
      'is authenticated': (r) => r.json().authenticated === true, // crashes. Will be displayed as successful anyway.
    })

    console.log('done')
  } catch (error) {
    console.error('Non-HTTP error, test aborted.', error)
    myTrend.add(1, { testId: testId, url: url, error: error })
  }
}

export default function(data) {
  const csrf = data.csrf
  console.log('csrf', csrf)
  // todo can you set this in setup?
  // todo We should get one cookie per VU.
/*  const jar = http.cookieJar()
  jar.set('http://127.0.0.1:8080/accueil/', 'csrftoken', csrf) // todo is url for whole site?
*/
  group('visit /accueil', function() {
    test('http://127.0.0.1:8080/accueil/', csrf)
  })
}
