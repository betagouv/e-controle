__docformat__ = "reStructuredText"
from dotenv import load_dotenv
import logging
import os
from wsgidav.fs_dav_provider import FilesystemProvider
from wsgidav._version import __version__
from wsgidav.wsgidav_app import DEFAULT_CONFIG, WsgiDAVApp


# Load the django environment : the webdav app is not a Django app, but it needs to query the django
# DB to get user permissions and allow or deby access to files.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecc.settings")
# Load the .env settings file to get environment variables
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path=env_path, override=True)
# Load the Django settings
from ecc import settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'ecc.settings'
import django
# Load Django
django.setup()

# Setup logger
logging.basicConfig(level=logging.DEBUG)

# Set up filesystem : we will serve the files that the Django server has saved to the MEDIA_ROOT
# folder.
rootpath = settings.MEDIA_ROOT
provider = FilesystemProvider(rootpath, readonly=True)

from webdav.cc_domain_controller import CCDomainController

# Create config for the WsgiDAVApp
config = DEFAULT_CONFIG.copy()
config.update({
  "provider_mapping": {"/": provider},
  "http_authenticator": {
    "domain_controller": CCDomainController,
    "accept_basic": True, "accept_digest": False,
    "default_to_digest": False,
  },
  "verbose": 4,
  "enable_loggers": [],
  "property_manager": True,  # True: use property_manager.PropertyManager
  "lock_manager": True,  # True: use lock_manager.LockManager
})

# Create WsgiDAVApp app
app = WsgiDAVApp(config)


# ?
def application(environ, start_response):
    return app(environ, start_response)
