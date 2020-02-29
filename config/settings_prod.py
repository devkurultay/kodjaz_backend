from .settings import *

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql_psycopg2',
       'NAME': 'lessons',
       'USER': 'online_teacher',
       'PASSWORD': 'codoMODOPostgresPassword2020',
       'HOST': 'localhost',
       'PORT': '',
   }
}

DEBUG = False

ALLOWED_HOSTS = ['codomodo.com']
