import pygame
import numpy


class Graphics:

    @staticmethod
    def initialisation():
        pygame.init()

    @staticmethod
    def new_window(width: int, height: int):
        pygame.display.set_mode((width, height))

    @staticmethod
    def quit_window():
        pygame.display.quit()

    @staticmethod
    def new_image(width: int, height: int):
        pygame.Surface((width, height))

    @staticmethod
    def load_sprite(path: str) -> pygame.Surface:
        return (pygame.image.load(path))

    def put_sprite_in_image(self, sprite_path: str, sprite_pos_x: int,
                            sprite_pos_y: int, sprite_width: int,
                            sprite_height: int):
        sprite = self.load_sprite(sprite_path)
        sprite_buffer = sprite.get_buffer().raw
        sprite_buffer = pygame.surfarray.pixels2d(sprite)
        # binary_buffer_sprite = 
        # print(format(sprite_buffer, "b"))
        print(sprite_buffer[100])
        # to put sprite to window we need
        # to get the sprite :
            # identify his pos_x and pos_y in sprite image
            # identify his width and height in sprite image
            # copy the pixel
        #to put it in the image buffer:
            #paste in the image buffer the sprite copy:
                # at pos_x, pox_y: paste each pixel in the buffer



