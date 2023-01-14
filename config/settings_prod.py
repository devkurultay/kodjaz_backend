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

DEBUG = os.environ.get('DEBUG')

ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOSTS')]
CSRF_TRUSTED_ORIGINS = ['https://' + os.environ.get('BACKEND_URL_ROOT', '')]

# PROD ONLY
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
