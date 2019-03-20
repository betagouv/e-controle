from wsgidav.fs_dav_provider import FilesystemProvider
from wsgidav._version import __version__
from wsgidav.wsgidav_app import DEFAULT_CONFIG, WsgiDAVApp
from webdav.ccomptes_dc import CCDomainController
__docformat__ = "reStructuredText"

#rootpath = gettempdir()
rootpath = "/opt/e-controle-media/"
provider = FilesystemProvider(rootpath)


config = DEFAULT_CONFIG.copy()
config.update({
    "provider_mapping": {"/": provider},
    "http_authenticator": {
        "domain_controller": CCDomainController,
        "accept_basic": True,
        "accept_digest": False,
        "default_to_digest": False,
    },
    "verbose": 4,
    "enable_loggers": [],
    "property_manager": True,  # True: use property_manager.PropertyManager
    "lock_manager": True,  # True: use lock_manager.LockManager
    })
app = WsgiDAVApp(config)

def application(environ, start_response):
    return app(environ, start_response)

