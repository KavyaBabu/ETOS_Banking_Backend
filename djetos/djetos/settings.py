"""
Django settings for djetos project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-r!(9*$fc_mti828qvh^4=c16+4*taw3elpyk65w3pl7ox!8&tz'

CLIENT_ID = 'pj33HMyuIyrjd7BpfCecEHQOcSMHDHOoeFaTpwjA'
CLIENT_SECRET = 'KxmM7LkmeRYMHsuSc5ZWLWvcoI0t9bkllKXaVTpzh2KK3PHjsrBErGN6I0tJDwsB63pzKGn01oklwkOqeBZLo2GkNSdvfoN6aepDSyLYiWLGpF2Db79a2v8tuJe81Huw'
GRANT_TYPE_PASSWORD = 'password'
GRANT_TYPE_REFRESH_TOKEN = 'refresh_token'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost','10.0.2.2','127.0.0.1','http://localhost:8081']

CORS_ALLOW_HEADERS = ['*']

CORS_ORIGIN_ALLOW_ALL = True


# Application definition

INSTALLED_APPS = [
    'corsheaders',  # this is for connecting bridge b/w api and server
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'rest_framework',
    'oauth2_provider',
    'django_filters',
    'drf_yasg',
    'users',
    'common_files',
    'general_app.account_opener'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'djetos.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

OAUTH2_PROVIDER = {
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope'},
    'ACCESS_TOKEN_EXPIRE_SECONDS': 36000
}

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.AllowAny',
    ),
    # 'PAGE_SIZE': 1000
}

# WSGI_APPLICATION = 'djetos.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ETOS_Banking',
        'USER': 'remote_user',
        'PASSWORD': 'ETOS@123',
        'HOST': '35.178.239.196',
        'PORT': '3306',
    },
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': 'testdb',
    #     'USER': 'psql_user1',
    #     'PASSWORD': 'Psql_2023',
    #     'HOST': '13.43.93.196',   # Or an IP Address that your DB is hosted on
    #     'PORT': '5432',
    # }
}
#
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'filters': {
#         'require_debug_false': {
#             '()': 'django.utils.log.RequireDebugFalse'
#         }
#     },
#     'formatters': {
#         'verbose': {
#             'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s'
#         },
#         'simple': {
#             'format': '[%(levelname)s] %(message)s'
#         },
#     },
#     'handlers': {
#         'file_django': {
#             'class': 'logging.FileHandler',
#             'filename': r'loginfo/file.log' + date.today().strftime('%Y%m%d') + '.log',
#             'formatter': 'verbose',
#             'level': 'ERROR'
#         },
#         # 'file_modules': {
#         #     'class': 'logging.FileHandler',
#         #     'filename': r'loginfo/log' + date.today().strftime('%Y%m%d') + '.log',
#         #     'formatter': 'verbose',
#         #     'level': 'ERROR'
#         # },
#         'mail_admins': {
#             'level': 'ERROR',
#             'filters': ['require_debug_false'],
#             'class': 'django.utils.log.AdminEmailHandler'
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file_django'],
#             'filename': r'loginfo/file.log' + date.today().strftime('%Y%m%d') + '.log',
#             'propagate': True,
#             'level': 'ERROR'
#         },
#         'django.request': {
#             'handlers': ['mail_admins'],
#             'level': 'ERROR',
#             'propagate': True,
#         },
#         # 'core.views': {
#         #     'handlers': ['file_modules'],
#         #     'propagate': True,
#         #     'level': 'ERROR'
#         # },
#     },
# }


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Email Setup

BASE_URL = 'http://127.0.0.1:8000/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'kavya@etos.co.uk'
EMAIL_HOST_PASSWORD = 'wwnc pnws kbwu fslj'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

AUTH_USER_MODEL = 'users.User'
LOGIN_URL = '/admin/login/'

CELERY_BROKER_URL = 'amqp://localhost'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'bulk_upload').replace('\\', '/')
MEDIA_URL = '/bulk_upload/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'