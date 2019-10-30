from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


try:
    from .dev import *
except ImportError:
    pass
