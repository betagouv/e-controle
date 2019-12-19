import encoding from 'k6/encoding'
import http from 'k6/http'
import { check, group, sleep } from 'k6'

export const options = {
  vus: 1,
  duration: '30s',
  throw: true,
}

const username = 'admin'
const password = 'faleco2019'

const serverUrl = 'http://127.0.0.1:8080/'
const adminPath = 'nonocat/'
const adminUrl = serverUrl + adminPath
const loginUrl = adminUrl + 'login/?next=/' + adminPath

const login = () => {
  // Get the csrf token : load the login form.
  console.log('Start login process')
  console.log('Getting login form for csrf token')
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
  console.log('Got login form.')

  // Get the csrf cookie from the form by regexing the page body.
  const found = res.body.match(/name="csrfmiddlewaretoken" value="(.*)"/)
  const formCsrf = found[1]
  console.log('csrf token from form', formCsrf)

  // Get the other csrf cookie from the response, and set it in cookies
  console.log('response cookies', JSON.stringify(res.cookies))
  const cookieCsrf = res.cookies.csrftoken[0].value
  console.log('Setting csrf cookie', cookieCsrf)
  const jar = http.cookieJar()
  jar.set(serverUrl, 'csrftoken', cookieCsrf)

  // Log in
  console.log('Making login request')
  const res2 = http.post(
    loginUrl,
    {
      csrfmiddlewaretoken: formCsrf,
      username: username,
      password: password,
    },
    {
      headers: {
        Referer: loginUrl,
      },
    },
  )
  console.log('response cookies', JSON.stringify(res2.cookies))
  console.log('authenticated?', JSON.stringify(res2.authenticated))
  if (res2.error || res2.error_code) {
    throw Error(res2.error_code + ' - ' + JSON.stringify(res2.error))
  }
  console.log('Done login request.')

  console.log('Final url : ', res2.url, 'expected : ', adminUrl)
  if (res2.url !== adminUrl) {
    throw Error('Login flow should end up on admin url : ' + adminUrl + ', but got : ' + res2.url)
  }

  console.log('done with login process.')
}

const test = (url) => {
  try {
    const res = http.get(url)

    if (res.error || res.error_code) {
      console.error('error', res.error_code, res.error)
    }

    console.log('Wanted', url, 'got redirected to', res.url)
    check(res, {
      'is status 200': (r) => r.status === 200,
      'no redirect': (r) => r.url === url,
    })

    console.log('done')
  } catch (error) {
    console.error('Non-HTTP error, test aborted.', error)
  }
}

// Setup is run only once, for all VUs. So you cannot do the login in setup, you need to login each user.
export function setup() {
  console.log('Running setup')
}

export default function(data) {
  // Start with the sleep so that you are sure it is run, even if the rest of the test crashes.
  // (to avoid DDOSing our own server!)
  sleep(0.1 + Math.random())

  group('login', () => {
    login()
  })
  sleep(1 + Math.random())

  group('visit /accueil', function() {
    test(serverUrl + 'accueil/')
  })
  sleep(1 + Math.random())

  group('visit some pages', function() {
    for (let i = 0; i < 10; i++) {
      test(serverUrl + 'accueil/')
      sleep(1 + Math.random() * 10)
      test(serverUrl + 'faq/')
      sleep(1 + Math.random() * 10)
    }
  })
}
