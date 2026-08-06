#game/scenes/game_mode_scene.py
from engine.core.scene import Scene
from engine.core.input import Input
from engine.utils.logger import Logger
from engine.game_registry import GameRegistry
from game.scenes.game_scene import GameScene
from games.tic_tac_toe.constants import (GAME_MODE_HUMAN_VS_HUMAN,GAME_MODE_HUMAN_VS_AI,)
import pygame
class GameModeScene(Scene):
    def __init__(self, game_name):
        super().__init__("Game Mode")
        self.game_name = game_name
        self.modes = [("Human vs Human", GAME_MODE_HUMAN_VS_HUMAN),("Human vs AI", GAME_MODE_HUMAN_VS_AI),]
        self.selected_index = 0
    def enter(self):
        super().enter()
        Logger.info(f"[GameModeScene] Choosing mode for {self.game_name}")
    def update(self):
        if Input.is_key_clicked(pygame.K_UP):
            self.selected_index = (self.selected_index - 1) % len(self.modes)
        elif Input.is_key_clicked(pygame.K_DOWN):
            self.selected_index = (self.selected_index + 1) % len(self.modes)
        elif Input.is_key_clicked(pygame.K_RETURN):
            mode_name, mode = self.modes[self.selected_index]
            Logger.info(f"[GameModeScene] Mode: {mode_name}")
            game_class = GameRegistry.get_game_class(self.game_name)
            game = game_class(renderer =self.renderer,game_mode=mode,)
            self.scene_manager.change_scene(GameScene(game))
    def render(self):
        self.renderer.draw_text(self.game_name, (80, 50), size=48,)
        self.renderer.draw_text("Select Mode", (80, 110), size=36, )
        y = 190
        for index, (mode_name, _) in enumerate(self.modes):
            prefix = "► " if index == self.selected_index else "  "
            self.renderer.draw_text( prefix + mode_name, (100, y), size=34, )
            y += 55