import logging
import logging.config
from pathlib import Path
from typing import Any


def get_logging_config(
        log_dir: Path, default_level: str = "INFO") -> dict[str, Any]:
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "console_format": {
                "format": "%(levelname)s - %(name)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            },
            "file_format": {
                "format": (
                    "%(asctime)s | %(name)s | [%(levelname)s] | %(message)s"),
                "datefmt": "%Y-%m-%d %H:%M:%S"
            },
            "detailed format": {
                "format": (
                    "%(asctime)s | %(name)s | [%(levelname)s] | "
                    "%(filename)s:%(lineno)d | %(message)s"
                ),
                "datefmt": "%Y-%m-%d %H:%M:%S"
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": default_level,
                "formatter": "console_format"
            },
            "file_main": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": str(log_dir / "pacman.log"),
                "maxBytes": 5242880,  # 5 Mo : 5 * 1024 * 1024,
                "backupCount": 1,
                "level": "DEBUG",
                "formatter": "detailed format",
                "encoding": "utf-8"
            },
            "file_errors": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": str(log_dir / "error.log"),
                "maxBytes": 1048576,  # 1 Mo
                "backupCount": 2,
                "level": "WARNING",
                "formatter": "detailed format",
                "encoding": "utf-8"
            },
        },
        "root": {
            "level": "DEBUG",
            "handlers": ["console", "file_main", "file_errors"]
        },
    }


def setup_logging(
        log_dir: Path | None = None, default_level: str = "INFO") -> None:
    """
    Applies the logging configuration using dictConfig.
    """
    if log_dir is None:
        project_root = Path(__file__).resolve().parent.parent
        log_dir = project_root / "logs"

    log_dir.mkdir(parents=True, exist_ok=True)
    config = get_logging_config(log_dir)
    logging.config.dictConfig(config)
