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
import { check, group, sleep } from 'k6'
import { Counter, Trend } from 'k6/metrics'

export const options = {
  /* Example 1 : during 30s, look through the script with 10 Virtual Users in parallel.
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
  vus: 1,
  duration: '30s',
  throw: true,
}

// Example metrics
const myCounter = new Counter('my_counter')
const myTrend = new Trend('my_trend')

const testId = Math.floor(Math.random() * 1000)

const username = 'inspector@demo.com'
const password = 'demoe12345'

const test = (url) => {
  // Start with the sleep so that you are sure it is run, even if the rest of the test crashes.
  // (to avoid DDOSing our own server!)
  sleep(1 + Math.random())

  try {
    const res = http.get(
      url,
      {
        headers: {
          Authorization: 'Basic ' + encoding.b64encode(`${username}:${password}`),
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

export default function() {
  group('visit login page', function() {
    test('http://127.0.0.1:8080/')
  })
  group('visit /accueil', function() {
    test('http://127.0.0.1:8080/accueil/')
  })
}
