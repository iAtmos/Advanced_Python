from filter import Filter
from handler_levels import HandlerLevels


dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    # "filters": {
    #   "filter": {
    #       "()": Filter
    #   }
    # },
    "formatters": {
        "base": {
            "format": "%(levelname)s | %(asctime)s | %(name)s | %(message)s",
            "datefmt": "%H:%M:%S"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "base"
        },
        "file": {
            "()": "logging.handlers.TimedRotatingFileHandler",
            "when": "h",
            "interval": 10,
            "backupCount": 5,
            "level": "INFO",
            "formatter": "base",
            # "filters": ["filter"],
            "filename": "logs/calculator.log",
        },
        "fileByLevels": {
            "()": HandlerLevels,
            "level": "DEBUG",
            "formatter": "base",
        }
    },
    "loggers": {
        "calculate_logger": {
            "level": "DEBUG",
            "handlers": ["file", "console"]
        },
        "web_data": {
            "level": "DEBUG",
            "handlers": ["fileByLevels", "console"]
        }
    }

    # "filters": {},
    # "root": {}
}