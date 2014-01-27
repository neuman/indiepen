"""
Django settings for indiepen project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'u#3nd=(+sya#!nnrawhrvn!9e0lh(@y3&4^hci=0+sqf%kbtwh'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

ANONYMOUS_USER_ID = 0


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'markdown_deux',
    'south',
    'djangobower',
    'core',
    'json_field',
    'tastypie',
    'taggit',
    'actstream',
    'guardian',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'indiepen.urls'

WSGI_APPLICATION = 'indiepen.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'djangobower.finders.BowerFinder',
)

PROJECT_ROOT = os.path.dirname(__file__)



BOWER_COMPONENTS_ROOT = os.path.join(BASE_DIR, 'static/bower_components')
BOWER_INSTALLED_APPS = (
    'jquery',
    'chartjs',
    'bootstrap',
    'bootstrap-switch',
    'dropzone',
    #'holder',
    'imagesloaded',
    'jquery.nicescroll',
    'jquery.scrollTo',
    'jquery.sparkline',
    'jquery.tagsinput',
    #'jquery.validate',
    'masonry',
    'oridomi',
    'underscore',
    'requirejs'
)


TEMPLATE_DIRS = (
  os.path.join(BASE_DIR, "templates"),
)

ACTSTREAM_SETTINGS = {
    'MODELS': ('core.project', 'core.post', 'core.pledge', 'core.media', 'core.options', 'auth.user', 'auth.group'),
}

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
from local_settings import *