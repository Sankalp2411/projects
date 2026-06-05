# engine/game_manager.py

import pygame

from engine.core.window import Window
from engine.core.renderer import Renderer


class GameManager:

    def __init__(self):

        self.running = False

        self.window = Window()

        self.renderer = Renderer()

    def initialize(self):

        print("[GameManager] Initializing...")

        self.window.create()

        self.renderer.initialize()

        self.running = True

    def run(self):

        print("[GameManager] Running...")

        while self.running:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False

            self.renderer.clear()

            self.window.update()

            self.window.tick(60)

    def shutdown(self):

        print("[GameManager] Shutting down...")

        self.renderer.shutdown()

        self.window.destroy()

        self.running = False