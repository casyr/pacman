import pygame
import numpy as np
from typing import Any
from ..errors import ViewError
from pathlib import Path


def initialisation() -> None:
    pygame.init()


def new_window(width: int, height: int) -> pygame.Surface:
    return pygame.display.set_mode((width, height))


def quit_window() -> None:
    pygame.quit()


def new_image(width: int, height: int) -> pygame.Surface:
    return pygame.Surface((width, height))


def update_window() -> None:
    pygame.display.update()


def load_sprite(path: Path) -> pygame.Surface:
    try:
        return pygame.image.load(path).convert_alpha()
    except FileNotFoundError as e:
        raise ViewError(e)
    except PermissionError as e:
        raise ViewError(e)


def blit_img(image: pygame.Surface,
             dest_screen: pygame.Surface,
             coords: tuple[int, int]) -> None:
    dest_screen.blit(image, coords)


def to_buffer(sprite: pygame.Surface,
              set_black_transparency: bool = True) -> np.ndarray:

    pixels = pygame.surfarray.pixels2d(sprite)

    if set_black_transparency:
        masks = sprite.get_masks()

        rgb_mask = masks[0] | masks[1] | masks[2]

        pixels[(pixels & rgb_mask) == 0] = 0

    return pixels.T.ravel()


def get_data_addr(image: pygame.Surface) -> np.ndarray:
    return pygame.surfarray.pixels2d(image)


def destroy_image(image: pygame.Surface) -> None:
    image.unlock()


def get_events() -> list[pygame.event.Event] | Any:
    return pygame.event.get()


def get_padding() -> int:
    return 500


def _get_key_mapping() -> dict[int, str]:
    return {
        pygame.K_w: "KEY_W",
        pygame.K_s: "KEY_S",
        pygame.K_a: "KEY_A",
        pygame.K_d: "KEY_D",
        pygame.K_p: "KEY_P",
        pygame.K_c: "KEY_C",
        pygame.K_1: "KEY_1",
        pygame.K_2: "KEY_2",
        pygame.K_3: "KEY_3",
        pygame.K_4: "KEY_4",
        pygame.K_5: "KEY_5",
        pygame.K_6: "KEY_6",
        pygame.K_BACKSPACE: "KEY_BACKSPACE",
        pygame.K_RETURN: "KEY_RETURN",
        pygame.K_SPACE: "KEY_SPACE"
    }


def get_key_pressed(event: pygame.event.Event) -> str | None:
    if event.type == pygame.KEYDOWN:
        mapping = _get_key_mapping()
        mapped_key = mapping.get(event.key, None)
        if mapped_key:
            return mapped_key
        is_letter = pygame.K_a <= event.key <= pygame.K_z
        is_number = pygame.K_0 <= event.key <= pygame.K_9
        is_space = event.key == pygame.K_SPACE
        if is_letter or is_number or is_space:
            char = chr(event.key)
            return f"CHAR_{char}"
    return None


def clear_window(window: pygame.Surface) -> None:
    window.fill((0, 0, 0))
