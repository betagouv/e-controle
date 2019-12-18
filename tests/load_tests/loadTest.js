/*
Install k6 to run this script : https://docs.k6.io/docs/installation
To make visualization graphs, you need InfluxDB and Grafana : https://docs.k6.io/docs/influxdb-grafana
Then run
k6 run --out influxdb=http://localhost:8086/myk6db <path to this script>
For more logging :
GODEBUG=http2debug=2 k6 run --out influxdb=http://localhost:8086/myk6db <path to this script>

View data in influxdb :
Talk to it in SQL, with a CLI (and format timestamps in rfc3339 to make them human-readable)
  influx -precision rfc3339
Select the db :
  USE mykydb
Lister les metrics loggées (https://docs.k6.io/docs/result-metrics#section-built-in-metrics) :
  SHOW measurements
Faire une query (attention, les valeurs de type string doivent etre 'quoted', et on peut "quoter" les noms mais pas obligé s'ils ne contiennent pas d'espaces)
  SELECT "error_code","url" FROM "http_reqs" WHERE time >= '2019-11-12T00:00:00Z' AND error_code='1404' Limit 5 tz('Europe/Paris')

*/

import http from 'k6/http'
import { check, sleep } from 'k6'
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

// const url = 'https://e-controle-pprod-beta.ccomptes.fr/'
const url = 'http://127.0.0.1:8080/accueil/'

const testId = Math.floor(Math.random() * 1000)

export default function() {
  // Start with the sleep so that you are sure it is run, even if the rest of the test crashes.
  // (to avoid DDOSing our own server!)
  sleep(1 + Math.random())

  try {
    const res = http.get(url)
    if (res.error || res.error_code) {
      console.error('error', res.error_code, res.error)
      myCounter.add(1, { testId: testId, url: url, error: res.error, error_code: res.error_code })
    }

    check(res, {
      'is status 200': (r) => r.status === 200,
    })
  } catch (error) {
    console.error('Non-HTTP error, test aborted.', error)
    myTrend.add(1, { testId: testId, url: url, error: error })
  }
}
