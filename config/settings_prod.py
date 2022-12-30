import os

from .settings import *

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql_psycopg2',
       'NAME': os.environ.get('DB_NAME'),
       'USER': os.environ.get('DB_USER'),
       'PASSWORD': os.environ.get('DB_PASSWORD'),
       'HOST': 'localhost',
       'PORT': '',
   }
}

DEBUG = os.environ.get('DEBUG')

ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOSTS')]
CSRF_TRUSTED_ORIGINS = ['https://' + os.environ.get('BACKEND_URL_ROOT', '')]

# PROD ONLY
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True