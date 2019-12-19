/*
Install k6 to run this script : https://docs.k6.io/docs/installation
Then run
k6 run <path to this script>

To make visualization graphs, you need InfluxDB and Grafana.
Follow install instructions : https://docs.k6.io/docs/influxdb-grafana
Then run :
k6 run --out influxdb=http://localhost:8086/myk6db <path to this script>

Debugging :
For more detailed logging :
GODEBUG=http2debug=2 k6 run --out influxdb=http://localhost:8086/myk6db <path to this script>
Log http headers : --http-debug
Log http request in full : --http-debug="full"
Run only one user and one iteration (overloads options in script) : -i 1 -u 1

View the data in influxdb :
Connect to db with CLI (and format timestamps in rfc3339 to make them human-readable)
  influx -precision rfc3339
Select the db :
  USE mykydb
List metrics that you logged (https://docs.k6.io/docs/result-metrics#section-built-in-metrics) :
  SHOW measurements
Make a query (warning : single-quote around strings values! Variable names can be double-quoted optionally.)
  SELECT "error_code","url" FROM "http_reqs" WHERE time >= '2019-11-12T00:00:00Z' AND error_code='1404' Limit 5 tz('Europe/Paris')

*/

import encoding from 'k6/encoding'
import http from 'k6/http'
import { check, fail, group, sleep } from 'k6'

export const options = {
  /* Example 1 : during 30s, loop through the script with 10 Virtual Users in parallel.
  vus: 10,
  duration: '30s',
  */
  /* Example 2
  stages: [
    // We start with zero users
    { duration: '3m', target: 10 }, // ramp up to 10 users
    { duration: '5m', target: 10 }, // stay at 10
    { duration: '10m', target: 35 }, // ramp up to 35
    { duration: '3m', target: 0 }, // ramp down to 0 users
  ],
  */
  /* Example 3 : run script 4 times, split between 2 VUs in parallel (so on average script runs 2 times per VU).
  vus: 2,
  iterations: 4,
  */
  vus: 2,
  iterations: 4,
}

const username = 'admin'
const password = 'faleco2019'

const serverUrl = 'http://127.0.0.1:8080/'
const adminPath = 'nonocat/'
const adminUrl = serverUrl + adminPath
const loginUrl = adminUrl + 'login/?next=/' + adminPath

// This functions creates and stores auth cookies, which are used in subsequent requests.
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
    fail(res.error_code + ' - ' + JSON.stringify(res.error))
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
    fail(res2.error_code + ' - ' + JSON.stringify(res2.error))
  }
  console.log('Done login request.')

  console.log('Final url : ', res2.url, 'expected : ', adminUrl)
  if (res2.url !== adminUrl) {
    fail('Login flow should end up on admin url : ' + adminUrl + ', but got : ' + res2.url)
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
    // Note : res.json() throws an error. Don't use it.

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
    for (let i = 0; i < 2; i++) {
      test(serverUrl + 'accueil/')
      sleep(1 + Math.random() * 10)
      test(serverUrl + 'faq/')
      sleep(1 + Math.random() * 10)
    }
  })
}
