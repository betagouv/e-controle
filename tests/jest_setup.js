// Import librairies for use in frontend tests.
// In the frontend pages, they are imported in <script> tags in the base template, so they are always present.
console.debug('Running jest setup')
import $ from 'jquery';
global.$ = global.jQuery = $;

require('../static/tabler/popper-1.12.9.min')
require('../static/tabler/bootstrap-4.0.0.min')

require('../static/tabler/core.js')

// Test util libs
const assert = require('assert')
global.assert = assert