import pygame
import numpy


class Graphics:

    @staticmethod
    def initialisation():
        pygame.init()

    @staticmethod
    def new_window(width: int, height: int):
        return (pygame.display.set_mode((width, height)))

    @staticmethod
    def quit_window():
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
        return (pygame.image.load(path))

    def put_sprite_in_image(self, dest_image: pygame.Surface,
                            dest_x: int, dest_y: int,
                            sprite_path: str, sprite_x: int, sprite_y: int,
                            sprite_width: int, sprite_height: int,
                            sprite_file_width: int, sprite_scale: int):

        sprite = self.load_sprite(sprite_path)
        sprite = sprite.convert(dest_image)

        sprite_buffer = pygame.surfarray.pixels2d(sprite).T.ravel()
        dest_image_buffer = pygame.surfarray.pixels2d(dest_image).T.ravel()

        screen_width = pygame.display.Info().current_w

        for y_gap in range(sprite_height * sprite_scale):
            for x_gap in range(sprite_width * sprite_scale):
                sprite_pos = ((((sprite_y + y_gap) // sprite_scale) *
                               sprite_file_width) +
                              ((sprite_x + x_gap) // sprite_scale))
                image_pos = (((dest_y + y_gap) * screen_width) +
                             (dest_x + x_gap))
                dest_image_buffer[image_pos] = sprite_buffer[sprite_pos]

#######main#######################################################################
    #from screeninfo import get_monitors
    #from src.view.graphics import Graphics

    # screen_width = get_monitors()[0].width
    #     screen_height = get_monitors()[0].height

    #     graphic = Graphics()
    #     graphic.initialisation()
    #     screen = graphic.new_window(screen_width, screen_height)
    #     image = graphic.new_image(screen_width, screen_height)
    #     graphic.put_sprite_in_image(image, 100, 100,
    #                                 "sprites/pacman_sprite.png",
    #                                 0, 0, 16, 16, 225, screen_width//900)

    #     run = True
    #     while (run):
    #         graphic.blit_img(image, screen, (0, 0))
    #         graphic.update_window()

    #     graphic.quit_window()
    #     return 0