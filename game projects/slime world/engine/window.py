import pygame


class GameWindow:
    def __init__(self, width: int = 1280, height: int = 720, title: str = "Slime World"):
        pygame.init()
        self.surface = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)

    def clear(self):
        self.surface.fill((15, 15, 20))

    def present(self):
        pygame.display.flip()
