/*
Install k6 to run this script : https://docs.k6.io/docs/installation
To make visualization graphs, you need InfluxDB and Grafana : https://docs.k6.io/docs/influxdb-grafana
Then run
k6 run --out influxdb=http://localhost:8086/myk6db <path to this script>
 */

import http from 'k6/http'
import { sleep } from 'k6'

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
  stages: [
    { duration: '3m', target: 300 },
    { duration: '3m', target: 0 },
  ],
}

export default function() {
  http.get('http://e-controle-dev-beta.ccomptes.fr/')
  sleep(1 + Math.random())
}
