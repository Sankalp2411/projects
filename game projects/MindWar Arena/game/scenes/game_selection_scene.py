#game/scenes/game_selection_scene.py
import pygame
from engine.core.scene import Scene
from engine.core.input import Input
from engine.utils.logger import Logger
from engine.game_registry import GameRegistry
from game.scenes.game_mode_scene import GameModeScene
class GameSelectionScene(Scene):
    def __init__(self):
        super().__init__("Game Selection")
        self.games = GameRegistry.get_game_names()
        self.selected_index = 0
    def enter(self):
        super().enter()
        Logger.info("[GameSelectionScene] Ready")
    def update(self):
        if Input.is_key_clicked(pygame.K_UP):
            self.selected_index = (self.selected_index - 1) % len(self.games)
        elif Input.is_key_clicked(pygame.K_DOWN):
            self.selected_index = (self.selected_index + 1) % len(self.games)
        elif Input.is_key_clicked(pygame.K_RETURN):
            selected_game = self.games[self.selected_index]
            Logger.info(f"[GameSelectionScene] Selected: {selected_game}")
            self.scene_manager.change_scene(GameModeScene(selected_game))
    def render(self):
        self.renderer.draw_text("Select Game",(80, 50),size=48,)
        y = 150
        for index, game in enumerate(self.games):
            prefix = "► " if index == self.selected_index else "  "
            self.renderer.draw_text(prefix + game,(100, y),size=36,)
            y += 55