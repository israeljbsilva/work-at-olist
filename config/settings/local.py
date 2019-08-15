"""
Local settings

- Run in Debug mode

- Use console backend for emails

- Add Django Debug Toolbar
- Add django-extensions as app
"""

import os
import socket

from .base import *  # noqa


# Debug mode
DEBUG = env.bool('DJANGO_DEBUG', default=True)
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG
TEMPLATES[0]['OPTIONS']['context_processors'].append('django.template.context_processors.debug')


# Secret key
SECRET_KEY = env('DJANGO_SECRET_KEY', default=')uzog$72o6s7tioh#!%c600z1!31ua$1=o*=zb!_-iho0v6gcd')


# CACHING
# ------------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}


INTERNAL_IPS = ['127.0.0.1', '0.0.0.0']


# tricks to have debug toolbar when developing with docker
if os.environ.get('USE_DOCKER') == 'yes':
    ip = socket.gethostbyname(socket.gethostname())
    INTERNAL_IPS += [ip[:-1] + '1']


# TESTING
# ------------------------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'


# Celery
CELERY_TASK_ALWAYS_EAGER = True
