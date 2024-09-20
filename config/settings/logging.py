import logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'vegeviewapp': {  # Replace with your app name
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
