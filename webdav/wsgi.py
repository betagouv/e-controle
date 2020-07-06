__docformat__ = "reStructuredText"
from dotenv import load_dotenv
import logging
import os
from wsgidav.fs_dav_provider import FilesystemProvider
from wsgidav._version import __version__
from wsgidav.wsgidav_app import DEFAULT_CONFIG, WsgiDAVApp

# Load the Django settings
from ecc import settings

def load_django_environment():
  """
  The webdav app is not a Django app, but it needs to query the django
  DB to get user permissions and allow or deby access to files.
  TODO can we move some imports to the top of the file ?
  """
  os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecc.settings")
  # Load the .env settings file to get environment variables
  BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  env_path = os.path.join(BASE_DIR, '.env')
  load_dotenv(dotenv_path=env_path, override=True)
  os.environ['DJANGO_SETTINGS_MODULE'] = 'ecc.settings'
  import django # TODO : this may need settings
  # Load Django
  django.setup()
load_django_environment()

print('loaded django')

logging.basicConfig(level=logging.DEBUG)

def make_filesystem_provider(django_settings):
  """
  Set up filesystem : we will serve the files that the Django server has saved to the MEDIA_ROOT
  folder.
  """
  rootpath = django_settings.MEDIA_ROOT
  provider = FilesystemProvider(rootpath, readonly=True)
  return provider
# TODO : does Django need to be loaded for this to work ?
provider = make_filesystem_provider(settings)

print('made filesystem provider')

# TODO : does django need to be loaded for this import to work ?
# Needs to import ecc and django.contrib
from webdav.cc_domain_controller import CCDomainController

def make_config(filesystem_provider, domain_controller_class):
  """
  Create config for the WsgiDAVApp
  """
  config = DEFAULT_CONFIG.copy()
  config.update({
    "provider_mapping": {"/": filesystem_provider},
    "http_authenticator": {
      "domain_controller": domain_controller_class,
      "accept_basic": True, "accept_digest": False,
      "default_to_digest": False,
    },
    "verbose": 4,
    "enable_loggers": [],
    "property_manager": True,  # True: use property_manager.PropertyManager
    "lock_manager": True,  # True: use lock_manager.LockManager
  })
  return config
config = make_config(provider, CCDomainController)

print('made config')

# Create WsgiDAVApp app
app = WsgiDAVApp(config)

print('made app. DONE')


# The webserver calls this function for each request in order to process it.
def application(environ, start_response):
  return app(environ, start_response)
