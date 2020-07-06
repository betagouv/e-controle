__docformat__ = "reStructuredText"
import django
from dotenv import load_dotenv
import logging
import os
from wsgidav.fs_dav_provider import FilesystemProvider
from wsgidav._version import __version__
from wsgidav.wsgidav_app import DEFAULT_CONFIG, WsgiDAVApp


def load_django_settings():
  # Load the .env settings file to get environment variables
  BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  env_path = os.path.join(BASE_DIR, '.env')
  load_dotenv(dotenv_path=env_path, override=True)
  # Load the Django settings (needs the .env variables, otherwise it will crash)
  os.environ['DJANGO_SETTINGS_MODULE'] = 'ecc.settings'
  from ecc import settings
  return settings


def load_django_environment(django_settings):
  """
  The webdav app is not a Django app, but it needs to query the django
  DB to get user permissions and allow or deby access to files.
  """
  # Note : You need to run load_django_settings first, otherwise this function will crash.
  # That is why the settings are required as argument to this function.
  django.setup()


def make_filesystem_provider(django_settings):
  """
  Set up filesystem : we will serve the files that the Django server has saved to the MEDIA_ROOT
  folder.
  """
  rootpath = django_settings.MEDIA_ROOT
  provider = FilesystemProvider(rootpath, readonly=True)
  return provider


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


# Create WsgiDAVApp app
logging.basicConfig(level=logging.DEBUG)
settings = load_django_settings()
load_django_environment(settings)
# Needs to import ecc.settings, otherwise it crashes.
# Needs Django to be imported and setup, otherwise crashes.
from webdav.cc_domain_controller import CCDomainController
provider = make_filesystem_provider(settings)
config = make_config(provider, CCDomainController)
app = WsgiDAVApp(config)


# The webserver calls this function for each request in order to process it.
def application(environ, start_response):
  return app(environ, start_response)
