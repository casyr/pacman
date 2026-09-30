from dataclasses import dataclass
from ..model import GameSession, GameBoard, HighScoreManager, LevelBuilder
from ..view import SpriteSheetsManager
from pygame import Surface


@dataclass
class GameContext:
    game_session: GameSession
    game_board: GameBoard
    level_manager: LevelBuilder
    highscores: HighScoreManager
