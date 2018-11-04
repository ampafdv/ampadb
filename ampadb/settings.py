"""
Django settings for ampadb project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

from .find_settings import AmpaDbSettings
import os
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_DIR)

_settings = AmpaDbSettings()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = _settings.get('secret_key')
if not SECRET_KEY:
    from django.utils.crypto import get_random_string
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    SECRET_KEY = get_random_string(50, chars)
    _settings.set('secret_key', SECRET_KEY)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = _settings.getboolean('debug', default=True)

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'ampadb_index.apps.AmpadbIndexConfig',
    'contactboard.apps.ContactboardConfig',
    'usermanager.apps.UsermanagerConfig',
    'importexport.apps.ImportexportConfig',
    'extraescolars.apps.ExtraescolarsConfig',
    'missatges.apps.MissatgesConfig',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'bootstrap3',
    'debug_toolbar',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

if DEBUG:
    INTERNAL_IPS = ['127.0.0.1']

ROOT_URLCONF = 'ampadb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'ampadb.support.context_processor',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ampadb.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

if _settings.get('database_url'):
    DATABASES['default'].update(
        dj_database_url.parse(_settings.get('database_url'), conn_max_age=500))
else:
    DATABASES['default'].update(dj_database_url.config(conn_max_age=500))

# Auth
LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'login'

# Seguretat
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True
HTTPS_ONLY = _settings.getboolean('https_only', default=False)
if HTTPS_ONLY:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = _settings.getint('hsts_seconds', 3600)
else:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_HSTS_SECONDS = 0

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
]

import importlib

if importlib.util.find_spec('bcrypt') is not None:
    PASSWORD_HASHERS.insert(
        0, 'django.contrib.auth.hashers.BCryptSHA256PasswordHasher')
    PASSWORD_HASHERS.insert(1,
                            'django.contrib.auth.hashers.BCryptPasswordHasher')

if importlib.util.find_spec('argon2') is not None:
    PASSWORD_HASHERS.insert(0,
                            'django.contrib.auth.hashers.Argon2PasswordHasher')

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        'OPTIONS': {
            'user_attributes': ['username']
        }
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 6
        }
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'ca'

LANGUAGES = [('ca', 'Català')]

TIME_ZONE = 'Europe/Madrid'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_ROOT = 'static'
STATIC_URL = '/static/'
STATICFILES_DIRS = ['dist']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Correu
# https://docs.djangoproject.com/en/1.10/topics/email/
DEFAULT_CHARSET = 'utf-8'
EMAIL_HOST = _settings.get('email_host')
EMAIL_PORT = _settings.getint('email_port')
EMAIL_HOST_USER = _settings.get('email_user')
EMAIL_HOST_PASSWORD = _settings.get('email_password')
EMAIL_USE_TLS = _settings.getboolean('email_tls', False)
EMAIL_USE_SSL = _settings.getboolean('email_ssl', False)
DEFAULT_FROM_EMAIL = _settings.get('from_email', EMAIL_HOST_USER)
SERVER_EMAIL = _settings.get('server_email', DEFAULT_FROM_EMAIL)
_ADMINS_raw = _settings.getjson('admins', {})
ADMINS = list(_ADMINS_raw.items())
_MANAGERS_raw = _settings.getjson('managers', {})
MANAGERS = list(_MANAGERS_raw.items())
