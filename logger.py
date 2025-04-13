from logging.config import dictConfig


def setup():
    dictConfig({
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)-4s %(funcName)s() L%(lineno)-4d %(message)s",
            },
            "detailed": {
                "format": "[%(asctime)s] %(levelname)-4s %(funcName)s() L%(lineno)-4d %(message)s - call_trace=%(pathname)s L%(lineno)-4d",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "gunicorn.error": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False,
            }
        },
        "root": {
            "handlers": ["console"],
            "level": "INFO",
        }
    })
