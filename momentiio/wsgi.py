"""
WSGI config for momentiio project.
It exposes the WSGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

application = get_wsgi_application()
application = DjangoWhiteNoise(application)
