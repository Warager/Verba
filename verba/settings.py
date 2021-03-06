"""
Django settings for verba project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import dj_database_url
# from verba.local_settings import SENDGRID_USER, SENDGRID_PASS/

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'oq*4w9=+qg#wh&)!_dq#h11d+c5m_(7y4y@j1q$mh(+7j2m2^b'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'verba.word_stats',
    'verba.accounts',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'verba.debug_middleware.ProcessExceptionMiddleware',
)

ROOT_URLCONF = 'verba.urls'

WSGI_APPLICATION = 'verba.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases


DATABASE_URL = 'sqlite:////{}/db.sqlite'.format(BASE_DIR)
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

DEFAULT_EMAIL = 'fomin.dritmy@gmail.com'

STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

try:
    from verba.local_settings import *  # noqa
except ImportError:
    SENDGRID_USER = ''
    SENDGRID_PASS = ''
    pass

DATABASES = {'default': dj_database_url.config(default=DATABASE_URL)}

SENDGRID_USERNAME = os.getenv('SENDGRID_USERNAME', SENDGRID_USER)
SENDGRID_PASSWORD = os.getenv('SENDGRID_PASSWORD', SENDGRID_PASS)
