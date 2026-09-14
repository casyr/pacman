import logging
import logging.config
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console_format": {
            "format": "%(levelname)s - %(name)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "file_format": {
            "format": "%(asctime)s | %(name)s | [%(levelname)s] | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "detailed format": {
            "format": (
                "%(asctime)s | %(name)s | [%(levelname)s] | "
                "%(filename)s:%(lineno)d | %(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "console_format"
        },
        "file_main": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(LOG_DIR / "pacman.log"),
            "maxBytes": 5242880,  # 5 Mo
            "backupCount": 1,
            "level": "DEBUG",
            "formatter": "detailed format",
            "encoding": "utf-8"
        },
        "file_errors": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(LOG_DIR / "error.log"),
            "maxBytes": 1048576,  # 1 Mo
            "backupCount": 2,
            "level": "WARNING",
            "formatter": "detailed format",
            "encoding": "utf-8"
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console", "file_main", "file_errors"]
    }
}


def setup_logging() -> None:
    """
    Applies the logging configuration using dictConfig.
    """
    logging.config.dictConfig(LOGGING_CONFIG)
