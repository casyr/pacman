import pygame
from ..errors import ViewError
from .sprite_sheet_manager import SpriteModel


class Graphics:

    @staticmethod
    def initialisation() -> None:
        pygame.init()

    @staticmethod
    def new_window(width: int, height: int) -> pygame.Surface:
        return (pygame.display.set_mode((width, height)))

    @staticmethod
    def quit_window() -> None:
        pygame.display.quit()

    @staticmethod
    def new_image(width: int, height: int) -> pygame.Surface:
        return (pygame.Surface((width, height)))

    @staticmethod
    def update_window() -> None:
        pygame.display.update()

    @staticmethod
    def blit_img(image: pygame.Surface, dest_screen: pygame.Surface,
                 coords: tuple[int, int]) -> None:
        dest_screen.blit(image, coords)

    @staticmethod
    def load_sprite(path: str) -> pygame.Surface:
        try:
            return (pygame.image.load(path))
        except FileNotFoundError as e:
            raise ViewError(e)
        except PermissionError as e:
            raise ViewError(e)

    def put_sprite_in_image(self, dest_image: pygame.Surface,
                            dest_x: int, dest_y: int,
                            sprite_data: SpriteModel,) -> None:

        scaling = 3

        sprite = sprite_data.sprite_surface.convert(dest_image)

        sprite_buffer = pygame.surfarray.pixels2d(sprite).T.ravel()
        dest_image_buffer = pygame.surfarray.pixels2d(dest_image).T.ravel()

        screen_width = pygame.display.Info().current_w

        sprite_data.pos_y *= scaling
        sprite_data.pos_x *= scaling
        for y_gap in range(sprite_data.height * scaling):
            for x_gap in range(sprite_data.width * scaling):
                sprite_pos = ((((sprite_data.pos_y + y_gap) // scaling) *
                               sprite_data.file_width) +
                              ((sprite_data.pos_x + x_gap) // scaling))
                image_pos = (((dest_y + y_gap) * screen_width) +
                             (dest_x + x_gap))
                if (sprite_buffer[sprite_pos] == 0):
                    dest_image_buffer[image_pos] = sprite_buffer[sprite_pos]
                    dest_image_buffer[image_pos] += 255
                else:
                    dest_image_buffer[image_pos] = sprite_buffer[sprite_pos]
