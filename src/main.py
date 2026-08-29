import sys
import logging
from exceptions import (
    PacmanError,
    ParsingError,
    ModelError,
    ViewError,
    ControllerError
)


def main() -> int:
    logger = logging.getLogger("MAIN")
    logger.info("Starting the application Pacman...")
    try:
        return 0

    except ParsingError as e:
        logger.error(f"Parsing failed:{e}")
        return 1

    except ModelError as e:
        logger.error(f"Raised during a logic rule forbidden.{e}")
        return 1

    except ViewError as e:
        logger.error(f"Graphics subsystem error : {e}")
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
        logger.critical(f"Unexpected Crash : {e}", exc_info=True)
        return 2


if __name__ == '__main__':
    sys.exit(main())
