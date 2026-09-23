# game/scenes/game_mode_scene.py
from __future__ import annotations
import pygame
from engine.core.input import Input
from engine.core.scene import Scene
from engine.game_registry import GameRegistry
from engine.utils.constants import GameMode
from engine.utils.logger import Logger
from game.scenes.game_scene import GameScene
class GameModeScene(Scene):
    MODES = [("Human vs Human", "Local 2-Player Match"),("Human vs AI", "Challenge Computer AI"),]
    TILE_WIDTH = 360
    TILE_HEIGHT = 180
    GAP = 60
    START_X = 250
    START_Y = 260
    def __init__(self, game_name: str) -> None:
        super().__init__("Game Mode")
        self.game_name = game_name
        self.selected_index = 0
        self.hovered_index = -1
    def enter(self) -> None:
        super().enter()
        Logger.info(f"[GameModeScene] Choosing mode for {self.game_name}")
    def _get_tile_rect(self, index: int) -> tuple[int, int, int, int]:
        x = self.START_X + index * (self.TILE_WIDTH + self.GAP)
        return (x, self.START_Y, self.TILE_WIDTH, self.TILE_HEIGHT)
    def update(self) -> None:
        mx, my = Input.get_mouse_position()
        self.hovered_index = -1
        for idx in range(len(self.MODES)):
            tx, ty, tw, th = self._get_tile_rect(idx)
            if tx <= mx <= tx + tw and ty <= my <= ty + th:
                self.hovered_index = idx
                self.selected_index = idx
                break
        if Input.is_left_mouse_clicked() and self.hovered_index >= 0:
            self._select_mode(self.hovered_index)
            return
        if Input.is_key_clicked(pygame.K_LEFT) or Input.is_key_clicked(pygame.K_a):
            self.selected_index = (self.selected_index - 1) % len(self.MODES)
        elif Input.is_key_clicked(pygame.K_RIGHT) or Input.is_key_clicked(pygame.K_d):
            self.selected_index = (self.selected_index + 1) % len(self.MODES)
        elif Input.is_key_clicked(pygame.K_ESCAPE) or Input.is_key_clicked(pygame.K_BACKSPACE):
            from game.scenes.main_menu_scene import MainMenuScene
            self.scene_manager.change_scene(MainMenuScene())
        elif Input.is_key_clicked(pygame.K_RETURN) or Input.is_key_clicked(pygame.K_SPACE):
            self._select_mode(self.selected_index)
    def _select_mode(self, index: int) -> None:
        title, _ = self.MODES[index]
        Logger.info(f"[GameModeScene] Selected mode: {title}")
        if title == "Human vs Human":
            game_class = GameRegistry.get_game_class(self.game_name)
            if game_class is None:
                Logger.error(f"[GameModeScene] Game not found: {self.game_name}")
                return
            try:
                game = game_class(renderer=self.renderer, game_mode=GameMode.HUMAN_VS_HUMAN.value)
            except TypeError:
                game = game_class(renderer=self.renderer)
            self.scene_manager.change_scene(GameScene(game))
        else:
            from game.scenes.difficulty_scene import DifficultyScene
            self.scene_manager.change_scene(DifficultyScene(self.game_name))
    def render(self) -> None:
        self.renderer.draw_text("Select the Mode", (475, 60), size=54, color=(255, 255, 255))
        self.renderer.draw_text(f"Game: {self.game_name}", (535, 135), size=26, color=(160, 185, 220))
        self.renderer.draw_text("[Esc] Back to Games", (80, 50), size=18, color=(140, 150, 170))
        for index, (title, subtitle) in enumerate(self.MODES):
            tx, ty, tw, th = self._get_tile_rect(index)
            is_active = (index == self.selected_index) or (index == self.hovered_index)
            if is_active:
                fill_color = (45, 75, 130)
                border_color = (120, 210, 255)
                title_color = (255, 255, 255)
                sub_color = (200, 225, 255)
            else:
                fill_color = (24, 28, 42)
                border_color = (55, 65, 88)
                title_color = (195, 205, 225)
                sub_color = (130, 140, 160)
            self.renderer.draw_filled_rectangle((tx, ty), (tw, th), fill_color)
            self.renderer.draw_rectangle((tx, ty), (tw, th), border_color)
            title_w = len(title) * 14
            title_x = max(tx + 10, tx + (tw - title_w) // 2)
            self.renderer.draw_text(title, (title_x, ty + 50), size=30, color=title_color)
            sub_w = len(subtitle) * 8
            sub_x = max(tx + 10, tx + (tw - sub_w) // 2)
            self.renderer.draw_text(subtitle, (sub_x, ty + 110), size=18, color=sub_color)