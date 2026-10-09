from dataclasses import dataclass, field
from ..model import GameSession, GameBoard, HighScoreManager, LevelBuilder
from ..view import GameView


@dataclass
class GameContext:
    """Shared game state and dependencies available to each scene.

    Attributes:
        game_session: Current session state and settings.
        game_board: Board for the current level.
        level_manager: Builder used to create levels.
        highscores: Manager for stored high scores.
        view: Game display and input handler.
    """

    game_session: GameSession
    game_board: GameBoard = field(init=False)
    level_manager: LevelBuilder
    highscores: HighScoreManager
    view: GameView
