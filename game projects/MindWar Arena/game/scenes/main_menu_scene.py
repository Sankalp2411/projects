from engine.core.scene import Scene
from engine.core.input import Input
from engine.utils.logger import Logger
from engine.game_registry import GameRegistry

from game.scenes.game_mode_scene import GameModeScene

import pygame


class MainMenuScene(Scene):

    def __init__(self):
        super().__init__("Main Menu")

        self.games = GameRegistry.get_game_names()
        self.selected_index = 0

    def enter(self):
        super().enter()
        Logger.info("[MainMenuScene] Ready")

    def update(self):

        if Input.is_key_clicked(pygame.K_UP):
            self.selected_index = (
                self.selected_index - 1
            ) % len(self.games)

        elif Input.is_key_clicked(pygame.K_DOWN):
            self.selected_index = (
                self.selected_index + 1
            ) % len(self.games)

        elif Input.is_key_clicked(pygame.K_RETURN):

            selected_game = self.games[self.selected_index]

            Logger.info(
                f"[MainMenuScene] Selected {selected_game}"
            )

            self.scene_manager.change_scene(
                GameModeScene(selected_game)
            )

    def render(self):

        self.renderer.draw_text(
            "MindWar Arena",
            (60, 40),
            size=54,
        )

        self.renderer.draw_text(
            "Select Game",
            (60, 110),
            size=38,
        )

        y = 190

        for index, game_name in enumerate(self.games):

            prefix = "► " if index == self.selected_index else "  "

            self.renderer.draw_text(
                prefix + game_name,
                (80, y),
                size=34,
            )

            y += 55