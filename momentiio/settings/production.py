import os
import dj_database_url
from .base import *

DEBUG = True

DATABASE_URL = os.environ.get('DATABASE_URL')
db_from_env = dj_database_url.config(
    default=DATABASE_URL, conn_max_age=500)

DATABASES['default'].update(db_from_env)
DATABASES['default'] = dj_database_url.config()
DATABASES['default']['CONN_MAX_AGE'] = 500

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = ['*', 'api-momentiio.herokuapp.com',
                 'http://www.momentiio.com', 'http://zealous-khorana-3e594f.netlify.com']

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

TEMPLATE_DEBUG = True
