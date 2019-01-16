"""
WSGI config for ecc project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

from dotenv import load_dotenv
import os
from libpath import Path

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecc.settings")

BASE_DIR = Path('.').parent.absolute()
env_path = BASE_DIR / '.env'
load_dotenv(dotenv_path=env_path, override=True)

application = get_wsgi_application()
