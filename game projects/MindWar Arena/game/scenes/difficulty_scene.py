# game/scenes/difficulty_scene.py
from __future__ import annotations
import pygame
from engine.core.input import Input
from engine.core.scene import Scene
from engine.game_registry import GameRegistry
from engine.utils.constants import Difficulty, GameMode
from engine.utils.logger import Logger
from game.scenes.game_scene import GameScene
class DifficultyScene(Scene):
    TILES = [("Beginner", Difficulty.BEGINNER, "Casual / Random"),("Easy", Difficulty.EASY, "Gentle play"),("Medium", Difficulty.MEDIUM, "Standard challenge"),("Hard", Difficulty.HARD, "Advanced tactics"),("Impossible", Difficulty.IMPOSSIBLE, "Master AI"),]
    TILE_WIDTH = 190
    TILE_HEIGHT = 160
    GAP = 22
    START_X = 125
    START_Y = 260
    def __init__(self, game_name: str) -> None:
        super().__init__("Difficulty Selection")
        self.game_name = game_name
        self.selected_index = 2
        self.hovered_index = -1
    def enter(self) -> None:
        super().enter()
        Logger.info(f"[DifficultyScene] Selecting difficulty for {self.game_name}")
    def _get_tile_rect(self, index: int) -> tuple[int, int, int, int]:
        x = self.START_X + index * (self.TILE_WIDTH + self.GAP)
        return (x, self.START_Y, self.TILE_WIDTH, self.TILE_HEIGHT)
    def update(self) -> None:
        mx, my = Input.get_mouse_position()
        self.hovered_index = -1
        for idx in range(len(self.TILES)):
            tx, ty, tw, th = self._get_tile_rect(idx)
            if tx <= mx <= tx + tw and ty <= my <= ty + th:
                self.hovered_index = idx
                self.selected_index = idx
                break
        if Input.is_left_mouse_clicked() and self.hovered_index >= 0:
            self._start_game(self.hovered_index)
            return
        if Input.is_key_clicked(pygame.K_LEFT) or Input.is_key_clicked(pygame.K_a):
            self.selected_index = (self.selected_index - 1) % len(self.TILES)
        elif Input.is_key_clicked(pygame.K_RIGHT) or Input.is_key_clicked(pygame.K_d):
            self.selected_index = (self.selected_index + 1) % len(self.TILES)
        elif Input.is_key_clicked(pygame.K_ESCAPE) or Input.is_key_clicked(pygame.K_BACKSPACE):
            from game.scenes.game_mode_scene import GameModeScene
            self.scene_manager.change_scene(GameModeScene(self.game_name))
        elif Input.is_key_clicked(pygame.K_RETURN) or Input.is_key_clicked(pygame.K_SPACE):
            self._start_game(self.selected_index)
    def _start_game(self, index: int) -> None:
        name, diff, _ = self.TILES[index]
        Logger.info(f"[DifficultyScene] Selected difficulty: {name} for {self.game_name}")
        game_class = GameRegistry.get_game_class(self.game_name)
        if game_class is None:
            Logger.error(f"[DifficultyScene] Game not found: {self.game_name}")
            return
        try:
            game = game_class(renderer=self.renderer, game_mode=GameMode.HUMAN_VS_AI.value, difficulty=diff)
        except TypeError:
            try:
                game = game_class(renderer=self.renderer, game_mode=GameMode.HUMAN_VS_AI.value)
            except TypeError:
                game = game_class(renderer=self.renderer)
        self.scene_manager.change_scene(GameScene(game))
    def render(self) -> None:
        self.renderer.draw_text("Select Difficulty", (470, 60), size=52, color=(255, 255, 255))
        self.renderer.draw_text(f"Game: {self.game_name}", (530, 130), size=26, color=(160, 185, 220))
        self.renderer.draw_text("[Esc] Back to Mode Selection", (80, 50), size=18, color=(140, 150, 170))
        for index, (title, _, desc) in enumerate(self.TILES):
            tx, ty, tw, th = self._get_tile_rect(index)
            is_active = (index == self.selected_index) or (index == self.hovered_index)
            if is_active:
                fill_color = (45, 75, 130)
                border_color = (120, 210, 255)
                title_color = (255, 255, 255)
                desc_color = (200, 230, 255)
            else:
                fill_color = (24, 28, 42)
                border_color = (55, 65, 88)
                title_color = (195, 205, 225)
                desc_color = (130, 140, 160)
            self.renderer.draw_filled_rectangle((tx, ty), (tw, th), fill_color)
            self.renderer.draw_rectangle((tx, ty), (tw, th), border_color)
            title_w = len(title) * 12
            title_x = max(tx + 8, tx + (tw - title_w) // 2)
            self.renderer.draw_text(title, (title_x, ty + 35), size=26, color=title_color)
            desc_w = len(desc) * 7
            desc_x = max(tx + 6, tx + (tw - desc_w) // 2)
            self.renderer.draw_text(desc, (desc_x, ty + 95), size=16, color=desc_color)