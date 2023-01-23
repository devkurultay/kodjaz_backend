import os
import dotenv
from datetime import timedelta
from pathlib import Path


ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent

DEV_LOCAL = 'dev_local'
DEV_ZAPPA = 'dev_zappa'
PROD_VPS = 'prod_vps'
PROD_ZAPPA = 'prod_zappa'

ENV = os.environ.get('ENV', DEV_LOCAL)
env_file = '.env'
if ENV == DEV_ZAPPA:
    env_file = '.env.zappa_dev'
elif ENV == PROD_ZAPPA:
    env_file = '.env.zappa_prod'
elif ENV == PROD_VPS:
    env_file = '.env.vps_prod'
dotenv.read_dotenv(ROOT_DIR / env_file)

SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG')

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(',')


INSTALLED_APPS_BASE = [
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

INSTALLED_APPS_OTHERS = [
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'dj_rest_auth',
    'dj_rest_auth.registration'
]

INSTALLED_APPS_LOCAL = [
    'authentication.apps.AuthenticationConfig',
    'users.apps.UsersConfig',
    'courses.apps.CoursesConfig',
    'frontend.apps.FrontendConfig',
    'crispy_forms',
    'drf_yasg',
]

INSTALLED_APPS = INSTALLED_APPS_BASE + INSTALLED_APPS_OTHERS + INSTALLED_APPS_LOCAL

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '1/minute'
    },
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=14),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer', 'Token',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [
            ROOT_DIR / 'templates',
            ROOT_DIR / 'courses/templates',
            ROOT_DIR / 'frontend/templates',
        ],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'markdown_extras': 'courses.templatetags.markdown_extras'
            },
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": os.environ.get('DB_HOST', 'localhost'),
        "PORT": 5432
    }
}

SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

LOGIN_REDIRECT_URL = "/"
ACCOUNT_ADAPTER = 'authentication.helpers.KodjazAccountAdapter'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_UNIQUE_EMAIL = True

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# We will create Laravel users in our DB. They are passed via JWT, which
# are created using the JWT_SECRET key
PASSWORD_HASHERS = [
    'authentication.hashers.CustomBCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    #'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
]


AUTH_USER_MODEL = 'users.User'


ST_SITE_URL = '/forum/'
# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Bishkek'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

# DEPRECATED(murat): remove STATIC_URL_BASE after migrating /cabinet code to the frontend repo
STATIC_URL_BASE = ''
STATIC_URL = '/static/'
STATIC_ROOT = str(ROOT_DIR / "staticfiles")
STATICFILES_DIRS = [str(ROOT_DIR / "static")]
MEDIA_URL = '/media/'
MEDIA_ROOT = ROOT_DIR / 'media'

# React.js stuff
FRONTEND_DIR = ROOT_DIR / 'frontend'
STATICFILES_DIRS += [
    FRONTEND_DIR / "build",
    FRONTEND_DIR / "build/static"
]

# DEPRECATED(murat): Remove after enabling prod frontend
OUTPUT_CONTAINER_ID_IN_EXERCISES_TEMPLATE = 'output'

# TODO(murat): review later
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_AGE = 86400 # 24 hours

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]
CORS_EXPOSE_HEADERS = ['Content-Type', 'X-CSRFToken']
CORS_ALLOW_CREDENTIALS = True

# For logging in a JWT user. localhost:8000/?token=jwt-tokenpyt
# We decrypt the passed jwt-token with this secret key
JWT_SECRET = os.environ.get('JWT_SECRET')

AWS_PYTHON_EXEC_LAMBDA_URL = os.environ.get('AWS_PYTHON_EXEC_LAMBDA_URL', '')
AWS_API_GATEWAY_API_KEY = os.environ.get('AWS_API_GATEWAY_API_KEY', '')

API_URL_ROOT = os.environ.get('API_URL_ROOT', '')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'kodjaz <app@kodjaz.com>'
DOMAIN_URL = os.environ.get('DOMAIN_URL', '')
