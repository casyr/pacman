class PacmanError(Exception):
    """Application base exception."""
    pass


class ParserError(PacmanError):
    """Raised during a argument read."""
    pass


class GameSettingsError(PacmanError):
    """Raised during a data read or validation error."""
    pass


class ModelError(PacmanError):
    """Raised during a rule are not allowed."""
    pass


class ViewError(PacmanError):
    """Raised during an initialization or graphics rendering failure."""
    pass


class ControllerError(PacmanError):
    """Raised during n controller failure."""
    pass
