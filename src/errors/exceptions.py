class PacmanError(Exception):
    """Base exception for application-specific failures."""


class GameSettingsError(PacmanError):
    """Raised when game settings cannot be read or validated."""


class ModelError(PacmanError):
    """Raised when game-model operations fail."""


class JsonLoadError(PacmanError):
    """Raised when JSON data cannot be accessed or written."""


class MazeError(ModelError):
    """Raised when maze generation fails."""


class LevelError(ModelError):
    """Raised when a game level cannot be built."""


class ViewError(PacmanError):
    """Raised when view initialization or rendering fails."""


class SpriteSheetError(ViewError):
    """Raised when sprite assets are missing or malformed."""


class ControllerError(PacmanError):
    """Raised when a controller operation fails."""
