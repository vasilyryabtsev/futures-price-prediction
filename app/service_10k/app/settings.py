from uvicorn.logging import DefaultFormatter
import os

os.makedirs('logs', exist_ok=True)

service_name = 'service_10k'

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            '()': DefaultFormatter,
            'format': "%(levelprefix)s %(message)s",
            'use_colors': True
        },
        'custom_formatter': {
            'format': f"%(asctime)s [{service_name}] [%(processName)s: %(process)d] [%(levelname)s] %(name)s: %(message)s",
        }
    },
    'handlers': {
        'default': {
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # По умолчанию stderr
        },
        'stream_handler': {
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'file_handler': {
            'formatter': 'custom_formatter',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/Log.log',
            'maxBytes': 1024 * 1024 * 1,  # = 1MB
            'backupCount': 3,
        },
    },
    'loggers': {
        'uvicorn': {
            'handlers': ['file_handler'],
            'level': 'TRACE',
            'propagate': False,
        },
        'uvicorn.access': {
            'handlers': ['file_handler'],
            'level': 'TRACE',
            'propagate': False,
        },
        'uvicorn.error': {
            'handlers': ['default', 'file_handler'],
            'level': 'TRACE',
            'propagate': False,
        },
        'uvicorn.asgi': {
            'handlers': ['file_handler'],
            'level': 'TRACE',
            'propagate': False,
        },
    },
}