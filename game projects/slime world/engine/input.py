import pygame


class InputHandler:
    def __init__(self):
        self.quit_requested = False

    def process_events(self):
        self.quit_requested = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_requested = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit_requested = True
