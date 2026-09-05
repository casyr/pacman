import pygame


def main():
    pygame.init()
    window = pygame.display.set_mode((800, 800))
    img = pygame.image.load("sprites/text_sprite.png")
    # screen = pygame.Surface((800, 800))
    while(True):
        window.blit(img, (400, 400))
        if (1 == 2):
            break

    pygame.display.quit()


if __name__ == "__main__":
    main()
