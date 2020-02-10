// Import librairies for use in frontend tests.
// In the frontend pages, they are imported in <script> tags in the base template, so they are always present.
import $ from 'jquery'
global.$ = global.jQuery = $

require('bootstrap')

require('../static/tabler/core.js')

// Test util libs
const assert = require('assert')
global.assert = assert
