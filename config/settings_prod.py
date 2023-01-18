import os
import sys
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .settings import *


DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql_psycopg2',
       'NAME': os.environ.get('AWS_DB_NAME'),
       'USER': os.environ.get('AWS_DB_USER'),
       'PASSWORD': os.environ.get('AWS_DB_PASSWORD'),
       'HOST': os.environ.get('AWS_DB_HOST'),
       'PORT': '',
   }
}

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.environ.get('AWS_REGION')
AWS_S3_CUSTOM_DOMAIN = '{}.s3.amazonaws.com'.format(AWS_STORAGE_BUCKET_NAME)
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
AWS_DEFAULT_ACL = 'public-read'
AWS_LOCATION = 'static'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
# DEPRECATED(murat): remove STATIC_URL_BASE after migrating /cabinet code to the frontend repo
STATIC_URL_BASE = 'https://{}'.format(AWS_S3_CUSTOM_DOMAIN)
STATIC_URL = '{}/{}/'.format(STATIC_URL_BASE, AWS_LOCATION)

DEBUG = False

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(',')
CSRF_TRUSTED_ORIGINS = ['https://' + os.environ.get('BACKEND_URL_ROOT', '')]

CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS').split(',')
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

sentry_sdk.init(
    dsn="https://5f64324425ce455fb3889116c1f61416@o4504467899940864.ingest.sentry.io/4504467902234624",
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.3,
    send_default_pii=True
)

# Logging
LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': ('%(levelname)s %(asctime)s %(name)s '
                       '%(message)s')
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'verbose'
        },
        'null': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'logging.NullHandler'
        },
    },
    'loggers': {
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
            'level': 'ERROR',
        },
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'authentication.apps.AuthenticationConfig': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'courses.apps.CoursesConfig': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'users.apps.UsersConfig': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
    },
}
