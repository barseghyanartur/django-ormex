from .base import *

LOGGING['loggers'].update(
    {
        'django.db': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        }
    }
)
