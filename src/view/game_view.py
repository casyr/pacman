import pygame
from . import mlx_wrapper as mlx
from screeninfo import get_monitors, ScreenInfoError


class GameView:
    def __init__(self) -> None:
        self.window: pygame.Surface | None = None
        self.assets: dict[str, pygame.Surface] = {}
        self.font: pygame.font.Font | None = None
        self.screen_width: int = 800
        self.screen_height: int = 600

    def initialize_graphics(self) -> None:
        mlx.initialisation()
        monitors = get_monitors()
        if not monitors:
            raise ScreenInfoError("No screen detected")
        screen = monitors[0]
        self.screen_width, self.screen_height = screen.width, screen.height
        mlx.new_window(self.screen_width, self.screen_height)

    def handle_events(self) -> str | None:
        key: str | None = None
        for event in mlx.get_events():
            print("Pygame event:", event)
            if event.type == pygame.QUIT:
                return "MOUSE_QUIT"
            action = mlx.get_key_pressed(event)
            if action is not None:
                key = action
        return key

    def close(self) -> None:
        mlx.quit_window()
