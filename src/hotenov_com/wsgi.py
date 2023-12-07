"""WSGI config for hotenov_com project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

# from django.core.wsgi import get_wsgi_application
from configurations.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hotenov_com.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "Dev")

application = get_wsgi_application()
