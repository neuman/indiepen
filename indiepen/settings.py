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
    'social.apps.django_app.default',
    'djcelery',
    'markdown_deux',
    'south',
    'djangobower',
    'core',
    'json_field',
    'tastypie',
    'taggit',
    'actstream',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

from django.contrib.messages import constants as message_constants
MESSAGE_TAGS = {
    message_constants.ERROR: 'danger'
}

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
    'requirejs',
)


TEMPLATE_DIRS = (
  os.path.join(BASE_DIR, "templates"),
)

ACTSTREAM_SETTINGS = {
    'MODELS': ('core.project', 'core.post', 'core.pledge', 'core.media', 'core.options', 'auth.user', 'auth.group', 'core.historicalproject','core.historicalpost','core.historicalmedia'),
    'USE_JSONFIELD':True,
}

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
from local_settings import *

try:
    stripe.api_key = STRIPE_SECRET_KEY
except Exception as e:
    STRIPE_PUBLIC_KEY = 'pk_test_gQYGUBwsm6rzvoSxBpSKbDC2'
    STRIPE_SECRET_KEY = 'sk_test_v3MTBY0TL2n2KjUCoGo7Sp23'

AUTH_PROFILE_MODULE = 'core.UserProfile'

#SOCIAL SOCIAL_AUTH
AUTHENTICATION_BACKENDS = (
  'social.backends.facebook.FacebookOAuth2',
  'django.contrib.auth.backends.ModelBackend',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/projects/create'
LOGIN_REDIRECT_URL = '/'

#celery / redis
BROKER_URL = 'redis://localhost:6379/0'
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}  # 1 hour.
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERYCONF = {'CELERY_ALWAYS_EAGER': True}
ELASTIC_TRANSCODER_PIPELINE_ID = '1395113752900-hi4huc'
ELASTIC_TRANSCODER_PIPELINE_NAME = 'indiepen_test'

