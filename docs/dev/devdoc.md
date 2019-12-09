# Architecture of the repo
Created 9 Dec 2019 - things could have changed since then, sorry :) Please add a date when you change sections of this doc. Place the date directly in the section you edited.

The README.md file also contains info on how things work, check it out.

## Database

Our backend is in Postgres. We define the tables through Django files. Look at : https://github.com/betagouv/e-controle/blob/develop/control/models.py and https://github.com/betagouv/e-controle/blob/develop/user_profiles/models.py for the main ones.

Here is the database schema - december 2019 :
https://github.com/betagouv/e-controle/blob/develop/docs/dev/e-controle-database.png

## Backend
The backend is in python, using Django. It is split up into several Django apps. We also have an API with Django Rest Framework.

### ecc
Root app. Contains the urls.py file (https://github.com/betagouv/e-controle/blob/develop/ecc/urls.py) which is useful to see how views are mapped to urls.

### control
Contains the main model (https://github.com/betagouv/e-controle/blob/develop/control/models.py) which is useful to understand the main objects in our database.

Most of the views are also there (https://github.com/betagouv/e-controle/blob/develop/control/views.py) : look at them to understand how the DB objects are passed into templates to the clients. The API views (used by Django REST API) are also there (https://github.com/betagouv/e-controle/blob/develop/control/api_views.py)


### Other things
#### Templates
The Django templates live in templates/ . We also use Vue.js (see below for details of how they interact).

#### Celery
Celery runs periodically to send out emails.

#### magicauth
We do not use passwords : we have email-based authentication. This is done by a module we developed called magicauth (https://github.com/betagouv/django-magicauth), in partnership with beta.gouv.fr.

## Frontend : static/
### General structure
The frontend uses Django templates and Vue.js. It is not a single page app.

Each page is loaded from server as a Django template (see templates/), which the django server fills with backend data. The served HTML page also contains javascript and CSS files.

Some of the javascript files are librairies that we use (e.g. bootstrap). Some are our own code, which are bundles of Vue.js code built with Parcel (see package.json for the build commandes, and README.md for details on how to use them.).

The design system and layout are done with Tabler (see static/tabler for the js and css that we use). Tabler is based on bootstrap, so many classes will be familiar to the bootstrap user. We do not use third-party component librairies : we make our own Vue.js components when needed, and use Tabler's CSS classes for styling and animations.

Our CSS is in static/css/custom.css and in Vue.js files (Vue.js allows declaring the CSS in the same file as the component, which makes it easy to track.).

Why this complex (and weird) Django+Vue structure? Because we started with only Django templates, and gradually added Vue as the JS became more complex and required it. We did not do a full rewrite as a Vue single-page app, but we are gradually working towards more Vue and less Django templates, so it could happen later. If it's not broken, don't fix it! :)

### An example of how Django templates and Vue interact : the control-detail page
 - The server serves the Django template at templates/ecc/control_detail.html. The corresponding view in the django code is ControlDetail (https://github.com/betagouv/e-controle/blob/develop/control/views.py#L30).
  - The django view fills in the template with data : controls_json, user_json, etc (everything in double brackets : {{ }}). Then send it to the client.
  - In the client, the JS file linked in the html gets (dist/control-detail-bundle.css) executed. This is Vue component, whose root file is https://github.com/betagouv/e-controle/blob/develop/static/src/control-detail.js.
   - The Vue root file loads the main component : https://github.com/betagouv/e-controle/blob/develop/static/src/controls/ControlPage.vue. It displays data that was passed as props from the django template. For example, the list of controls was passed at https://github.com/betagouv/e-controle/blob/develop/templates/ecc/control_detail.html#L7, and becomes the prop at https://github.com/betagouv/e-controle/blob/develop/static/src/controls/ControlPage.vue#L64.
   - From then on, it's normal Vue code :)

   Note that on the same page, there are other Vue bundles loaded : the sidebar bundle (https://github.com/betagouv/e-controle/blob/develop/templates/base.html#L74) which displays the left side menu, and the session management bundle (https://github.com/betagouv/e-controle/blob/develop/templates/base.html#L84) which logs out the user after a time.

   Each bundle is a separate JS file, and they do now have shared variables.

### Parcel bundles
We have several Parcel bundles, which are linked and run in several pages. The bundles are generated in the src/dist directory. Each Parcel build generates a JS and a CSS files, which you can see linked in the Django templates. (some bundles have no CSS, in which case it's just a JS file.)

#### sidebar-bundle.js and sidebar-bundle.css
Linked on every page (or almost). This displays the menu sidebar on the left. It fetches the data to fill the sidebar with a backend call (using the axios library).

#### session-management-bundle.js
Linked on every page (from the base django template https://github.com/betagouv/e-controle/blob/develop/templates/base.html#L84). It sets a timer, and after a given time it will log out the user unless they take action.

#### control-detail-bundle.js and control-detail-bundle.css
Displays each control ("Espace de dépôt").

Root file : https://github.com/betagouv/e-controle/blob/develop/static/src/control-detail.js

When the user clicks in the menu, it changes the displayed control and the hash in the URL, without server reload, in this same Vue bundle (like a kind of mini multi-page app...)

The component gets the list of controls and the current user from server through the Django template (see "An example" for details). Additional backend calls are made in various sub-components, to get more data or to update it.

#### questionnaire-detail-bundle.js and questionnaire-detail-bundle.css
Displays a questionnaire. Straightforward.

Root file : https://github.com/betagouv/e-controle/blob/develop/static/src/questionnaire-detail.js

#### questionnaire-create-bundle.js and questionnaire-create-bundle.css
Displays a Wizard in 3 steps for creating a questionnaire. No server reload between the wizard steps (mini multi-page app).

Root file : https://github.com/betagouv/e-controle/blob/develop/static/src/questionnaire-create.js


### Vue subcomponents
In the folders in static/src, the Vue components.
