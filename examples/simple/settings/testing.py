import os
from .base import *  # NOQA

IS_TRAVIS = 'TRAVIS' in os.environ

SQLITE_DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': PROJECT_DIR(os.path.join('..', '..', 'db', 'example.db')),
    }
}

MYSQL_DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ormex',
        'USER': 'root',
        'PASSWORD': '' if IS_TRAVIS else 'test',
        # Empty for localhost through domain sockets or '127.0.0.1' for
        # localhost through TCP.
        'HOST': '',
        # Set to empty string for default.
        'PORT': '',
    }
}

POSTGRESQL_DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ormex',
        'USER': 'postgres',
        'PASSWORD': '' if IS_TRAVIS else 'test',
        # Empty for localhost through domain sockets or '127.0.0.1' for
        # localhost through TCP.
        'HOST': '',
        # Set to empty string for default.
        'PORT': '',
    }
}

DATABASES = POSTGRESQL_DATABASES

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['all_log'],
    },
    'formatters': {
        'verbose': {
            'format': '\n%(levelname)s %(asctime)s [%(pathname)s:%(lineno)s] '
                      '%(message)s'
        },
        'simple': {
            'format': '\n%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'all_log': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': PROJECT_DIR("../../logs/all.log"),
            'maxBytes': 1048576,
            'backupCount': 99,
            'formatter': 'verbose',
        },
        'django_log': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': PROJECT_DIR("../../logs/django.log"),
            'maxBytes': 1048576,
            'backupCount': 99,
            'formatter': 'verbose',
        },
        'django_request_log': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': PROJECT_DIR("../../logs/django_request.log"),
            'maxBytes': 1048576,
            'backupCount': 99,
            'formatter': 'verbose',
        },
        'i18next_log': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': PROJECT_DIR("../../logs/i18next.log"),
            'maxBytes': 1048576,
            'backupCount': 99,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['django_request_log'],
            'level': 'INFO',
            'propagate': True,
        },
        'django': {
            'handlers': ['django_log'],
            'level': 'ERROR',
            'propagate': False,
        },
        'i18next': {
            'handlers': ['console', 'i18next_log'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
