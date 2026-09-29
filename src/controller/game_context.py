from dataclasses import dataclass
from ..model import GameSession, GameBoard, HighScoreManager, LevelBuilder
from ..view import SpriteSheetsManager
from pygame import Surface


@dataclass
class GameContext:
    game_session: GameSession
    game_board: GameBoard | None
    level_manager: LevelBuilder
    highscores: HighScoreManager
    sprite_sheets: SpriteSheetsManager
    window: Surface
    screen_width: int
    screen_height: int
