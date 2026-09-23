import pygame
from ..errors import ViewError
from functools import lru_cache


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


def load_sprite(path: str) -> pygame.Surface:
    try:
        return (pygame.image.load(path))
    except FileNotFoundError as e:
        raise ViewError(e)
    except PermissionError as e:
        raise ViewError(e)


def blit_img(image: pygame.Surface,
             dest_screen: pygame.Surface,
             coords: tuple[int, int]) -> None:
    dest_screen.blit(image, coords)


def get_events() -> list:
    return pygame.event.get()


def check_quit_event(event: pygame.event.Event) -> bool:
    if event.type == pygame.QUIT:
        return True
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        return True
    return False


@lru_cache(maxsize=1)
def _get_key_mapping() -> dict[int, str]:
    return {
        pygame.K_w: "KEY_UP",
        pygame.K_s: "KEY_DOWN",
        pygame.K_a: "KEY_LEFT",
        pygame.K_d: "KEY_RIGHT",
        pygame.K_p: "KEY_PAUSED",
        pygame.K_c: "KEY_CHEAT_MENU",
        pygame.K_1: "START_KEY",
        pygame.K_2: "HIGHSCORES_KEY",
        pygame.K_3: "INSTRUCTION_KEY",
        pygame.K_4: "EXIT_KEY",
        pygame.K_KP1: "START_KEY",
        pygame.K_KP2: "HIGHSCORES_KEY",
        pygame.K_KP3: "INSTRUCTION_KEY",
        pygame.K_KP4: "EXIT_KEY",
    }


def get_key_pressed(event: pygame.event.Event) -> str | None:
    if event.type == pygame.KEYDOWN:
        mapping = _get_key_mapping()
        return mapping.get(event.key, None)
    return None
