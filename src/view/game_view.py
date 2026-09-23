import pygame
from . import mlx_wrapper as mlx
from screeninfo import get_monitors, ScreenInfoError
# from .sprite_sheet_manager import SpriteModel


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
            if mlx.check_quit_event(event):
                return "EXIT_KEY"
            action = mlx.get_key_pressed(event)
            if action is not None:
                key = action
        return key

    def close(self) -> None:
        mlx.quit_window()

    # def put_sprite_in_image(self, dest_image: pygame.Surface,
    #                         dest_x: int, dest_y: int,
    #                         sprite_data: SpriteModel,) -> None:

    #     scaling = 3

    #     sprite = sprite_data.sprite_surface.convert(dest_image)

    #     sprite_buffer = pygame.surfarray.pixels2d(sprite).T.ravel()
    #     dest_image_buffer = pygame.surfarray.pixels2d(dest_image).T.ravel()

    #     screen_width = pygame.display.Info().current_w

    #     sprite_data.pos_y *= scaling
    #     sprite_data.pos_x *= scaling
    #     for y_gap in range(sprite_data.height * scaling):
    #         for x_gap in range(sprite_data.width * scaling):
    #             sprite_pos = ((((sprite_data.pos_y + y_gap) // scaling) *
    #                            sprite_data.file_width) +
    #                           ((sprite_data.pos_x + x_gap) // scaling))
    #             image_pos = (((dest_y + y_gap) * screen_width) +
    #                          (dest_x + x_gap))
    #             dest_image_buffer[image_pos] = sprite_buffer[sprite_pos]
