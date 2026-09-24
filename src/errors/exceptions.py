class PacmanError(Exception):
    """Application base exception."""


class GameSettingsError(PacmanError):
    """Raised during a data read or validation error."""


class ModelError(PacmanError):
    """Raised during a rule are not allowed."""


class JsonLoadError(PacmanError):
    """Raised during write a Json file."""


class MazeError(ModelError):
    """Raised during call to maze_generator"""


class LevelError(ModelError):
    """Raised during build a level"""


class ViewError(PacmanError):
    """Raised during an initialization or graphics rendering failure."""


class SpriteSheetError(ViewError):
    """
    This error type in inheritance to ViewError
    and raised his own error in case of:
        - fail to laod sprite data
        - malformed file
    """


class ControllerError(PacmanError):
    """Raised during n controller failure."""
