import logging
from pydantic import BaseModel

# from src.exceptions import ParsingError

logger = logging.getLogger(__name__)


class GameSettings(BaseModel):
    pass
