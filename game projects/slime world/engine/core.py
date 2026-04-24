# engine/core.py

import pygame
from engine.clock import GameClock
from engine.input import InputHandler
from engine.renderer import Renderer
from engine.window import GameWindow
from config import settings


class Engine:
    def __init__(self, game):
        pygame.init()

        self.window = GameWindow()
        self.clock = GameClock(settings.FPS)
        self.input = InputHandler()
        self.renderer = Renderer(self.window.surface)

        self.game = game
        self.running = True

    def run(self):
        while self.running:
            self.input.update()
            if self.input.quit_requested:
                self.running = False

            dt = self.clock.tick()
            self.game.update(dt)

            self.window.clear()
            self.game.render(self.renderer)
            self.renderer.flush()
            self.window.present()

        self.shutdown()

    def shutdown(self):
        pygame.quit()
