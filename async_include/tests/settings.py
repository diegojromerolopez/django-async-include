# -*- coding: utf-8 -*-

import os
import sys

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
ASYNC_INCLUDE_PATH = os.path.normpath(os.path.join(BASE_PATH, '..', '..'))
if ASYNC_INCLUDE_PATH not in sys.path:
    sys.path.insert(0, ASYNC_INCLUDE_PATH)

SECRET_KEY = "secret-key"

TEST_DATABASE_PATH = os.path.join(BASE_PATH, "resources/test.db")


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': TEST_DATABASE_PATH
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_PATH+"/templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]

INSTALLED_APPS = [
    'async_include',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin'
]

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'crequest.middleware.CrequestMiddleware',
    'cuser.middleware.CuserMiddleware'
)

ROOT_URLCONF = 'async_include.tests.urls'
