"""
WSGI config for ecc project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
from pathlib import Path

from dotenv import load_dotenv

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecc.settings")

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path, override=True)

application = get_wsgi_application()
