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
                            sprite_width: int, sprite_height: int):

        sprite = self.load_sprite(sprite_path)
        sprite = sprite.convert(dest_image)

        sprite_buffer = pygame.surfarray.pixels2d(sprite).T.ravel()
        dest_image_buffer = pygame.surfarray.pixels2d(dest_image).T.ravel()
        # print(sprite_buffer.dtype)

        for y_gap in range(sprite_height):
            for x_gap in range(sprite_width):
                sprite_pos = (((sprite_y + y_gap) * 224) + ((sprite_x + x_gap) * (64/8)))
                image_pos = (((dest_y + y_gap) * 800) + ((dest_x + x_gap) * (64/8)))
                dest_image_buffer[image_pos] = sprite_buffer[sprite_pos]
        # print(sprite_buffer)
        # for i in range(len(224)):
        #     for j in range(len(124)):
        #         dest_image[i][j]
        # to put sprite to window we need
        # to get the sprite :
            # identify his pos_x and pos_y in sprite image
            # identify his width and height in sprite image
            # copy the pixel
        #to put it in the image buffer:
            #paste in the image buffer the sprite copy:
                # at pos_x, pox_y: paste each pixel in the buffer
