import sys
import json
from pathlib import Path
from exceptions import ConfigError
import logging

logger = logging.getLogger(__name__)


def parse_cli_args() -> Path:
    args = sys.argv[1:]
    if len(args) == 0:
        raise ConfigError("Missing argument: please provide a JSON "
                          "configuration file.")
    if len(args) > 1:
        raise ConfigError(f"Too many arguments: expected 1, "
                          f"received {len(args)}.")
    return Path(args[0])


def load_and_validate_config(file_path: Path) -> dict:
    if file_path.suffix.lower() != ".json":
        raise ConfigError("file must be a .json only !")
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        raise ConfigError(f"File not found: '{file_path}'.")
    except PermissionError:
        raise ConfigError(f"Permission reading denied: '{file_path}'.")
    except json.JSONDecodeError as e:
        raise ConfigError(f"Format JSON invalid '{file_path}' "
                          f"(line {e.lineno}) : {e.msg}.")
    return data
