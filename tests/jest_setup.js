// Import librairies for use in frontend tests.
// In the frontend pages, they are imported in <script> tags in the base template, so they are always present.
console.debug('Running jest setup')
import $ from 'jquery';
global.$ = global.jQuery = $;

// todo bootstrap
