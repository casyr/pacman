from dataclasses import dataclass, field
from ..model import GameSession, GameBoard, HighScoreManager, LevelBuilder
from ..view import GameView


@dataclass
class GameContext:
    game_session: GameSession
    game_board: GameBoard = field(init=False)
    level_manager: LevelBuilder
    highscores: HighScoreManager
    view: GameView
