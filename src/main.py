import sys
import logging
from utils.config_logging import setup_logging
from cli import parse_cli_args, load_and_validate_config
from exceptions import (
    PacmanError,
    ConfigError,
    ParsingError,
    ModelError,
    ViewError,
    ControllerError
)


def main() -> int:
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting the application Pacman...")

    try:
        config_path = parse_cli_args()
        data = load_and_validate_config(config_path)
        logger.debug({data})
        return 0
    except ConfigError as e:
        logger.error(f"CLI failed: {e}")
        return 1
    except ParsingError as e:
        logger.error(f"Parsing failed: {e}")
        return 1

    except ModelError as e:
        logger.error(f"Raised during a logic rule forbidden: {e}")
        return 1

    except ViewError as e:
        logger.error(f"Graphics subsystem error: {e}")
        return 1

    except ControllerError as e:
        logger.error(f"Controller subsystem error: {e}")
        return 1

    except PacmanError as e:
        logger.error(f"Application Pacman error: {e}")
        return 1

    except KeyboardInterrupt:
        logger.warning("Manual interruption by the user.")
        return 130

    except Exception as e:
        logger.critical(f"Unexpected Crash: {e}", exc_info=True)
        return 2


if __name__ == '__main__':
    sys.exit(main())
