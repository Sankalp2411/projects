import pygame
import sys
import time


class GameLoop:
    def __init__(self, update_callback, render_callback, width=800, height=600):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Slime World")

        self.clock = pygame.time.Clock()
        self.update_callback = update_callback
        self.render_callback = render_callback
        self.running = True

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            self.update_callback(dt)
            self.render_callback(self.screen)

            pygame.display.flip()

        pygame.quit()
        sys.exit()
