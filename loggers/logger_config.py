# config.py
import logging

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'file_handler': {
            'class': 'logging.FileHandler',
            'filename': 'app.log',
            'formatter': 'standard',
            'level': logging.INFO,
        },
    },
    'loggers': {
        'user_logger': {
            'handlers': ['file_handler'],
            'level': logging.INFO,
            'propagate': False,
        },
        'message_logger': {
            'handlers': ['file_handler'],
            'level': logging.INFO,
            'propagate': False,
        },
        'connection_logger': {
            'handlers': ['file_handler'],
            'level': logging.INFO,
            'propagate': False,
        },
    },
}
