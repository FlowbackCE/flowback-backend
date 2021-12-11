# FlowBack was created and project lead by Loke Hagberg. The design was
# made by Lina Forsberg. Emilio Müller helped constructing Flowback.
# Astroneatech created the code. It was primarily financed by David
# Madsen. It is a decision making platform.
# Copyright (C) 2021  Astroneatech AB
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see https://www.gnu.org/licenses/.

"""
Django settings for superadmin project.

Generated by 'django-admin startproject' using Django 1.11.20.z

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from dotenv import load_dotenv
load_dotenv()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# import dj_database_url
import environ

BASE_DIR = os.path.dirname((os.path.dirname(__file__)))
print(BASE_DIR)
env = environ.Env(DEBUG=(bool, False))
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#
SECRET_KEY = os.getenv("DJANGO_SECRET")

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # http://www.django-rest-framework.org/
    'rest_framework.authtoken',
    'django_rest_passwordreset',
    'django_extensions',
    'django_inlinecss',
    'drf_yasg',
    'taggit',
    'flowback.base',
    'flowback.users',
    'flowback.polls',
    'flowback.notifications',
    'whitenoise.runserver_nostatic',
    'channels',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = "settings.urls"

TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
print(TEMPLATES_DIR)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ]
        },
    },
]

WSGI_APPLICATION = "settings.wsgi.application"
ASGI_APPLICATION = "settings.asgi.application"
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

# DATABASES = {
#      'default': {
#          'ENGINE': 'django.db.backends.postgresql',
#
#          'NAME': 'wwt',
#          'USER': 'postgres',
#          'PASSWORD': '0000',
#          'HOST': env('FLOWBACK_DB_HOST', default='localhost'),  # Or an IP Address that your DB is hosted on
#
#      }
#  }

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.sqlite3',
       'NAME': os.path.join(BASE_DIR, "db.sqlite3"),
   }
}

#db_from_env = dj_database_url.config(conn_max_age=600)
#DATABASES['default'].update(db_from_env)
# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator", },
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator", },
]

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend" if not DEBUG else \
                 "django.core.mail.backends.dummy.EmailBackend"
EMAIL_HOST = env('EMAIL_HOST', default='<smtp.yourserver.com>')
EMAIL_PORT = env('EMAIL_PORT', default='<your-server-port>')
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='<your-email>')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='<your-email-password>')
EMAIL_USE_TLS = env('EMAIL_USE_TLS', default=True)
EMAIL_USE_SSL = env('EMAIL_USE_SSL', default=False)
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = False

AUTH_USER_MODEL = 'users.User'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_URL = '/static/'
print(STATIC_URL)
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
print(BASE_DIR)
print(STATIC_ROOT)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
SESSION_COOKIE_NAME = 'sessionid_flowback'

# ──┤ API ├───────────────────────────────────────────────────────────────────┐
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'flowback.base.api.pagination.PageNumberPagination',
    'PAGE_SIZE': 30,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'flowback.users.auth.backend.EmailBackend',
)

DEVELOPMENT_ENVIRONMENT = env('DEVELOPMENT_ENVIRONMENT', default='local')

CORS_ALLOW_ALL_ORIGINS = True  # allow cors requests

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
