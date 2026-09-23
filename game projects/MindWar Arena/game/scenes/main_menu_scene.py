# game/scenes/main_menu_scene.py
from __future__ import annotations
import pygame
from engine.core.input import Input
from engine.core.scene import Scene
from engine.utils.logger import Logger
from game.scenes.game_mode_scene import GameModeScene
class MainMenuScene(Scene):
    GRID_COLS = 3
    GRID_ROWS = 3
    TILE_WIDTH = 280
    TILE_HEIGHT = 110
    GAP_X = 40
    GAP_Y = 25
    START_X = 180
    START_Y = 175
    ORDERED_GAMES = ["Tic-Tac-Toe","Connect Four","Gomoku","Pente","Othello","Checkers","Chess","Nine Men's Morris","Go",]
    def __init__(self) -> None:
        super().__init__("Main Menu")
        self.games = self.ORDERED_GAMES
        self.selected_index = 0
        self.hovered_index = -1
    def enter(self) -> None:
        super().enter()
        Logger.info("[MainMenuScene] Main Menu ready with 3x3 game grid")
    def _get_tile_rect(self, index: int) -> tuple[int, int, int, int]:
        row = index // self.GRID_COLS
        col = index % self.GRID_COLS
        x = self.START_X + col * (self.TILE_WIDTH + self.GAP_X)
        y = self.START_Y + row * (self.TILE_HEIGHT + self.GAP_Y)
        return (x, y, self.TILE_WIDTH, self.TILE_HEIGHT)
    def update(self) -> None:
        mx, my = Input.get_mouse_position()
        self.hovered_index = -1
        for idx in range(len(self.games)):
            tx, ty, tw, th = self._get_tile_rect(idx)
            if tx <= mx <= tx + tw and ty <= my <= ty + th:
                self.hovered_index = idx
                self.selected_index = idx
                break
        if Input.is_left_mouse_clicked() and self.hovered_index >= 0:
            self._select_game(self.hovered_index)
            return 
        if Input.is_key_clicked(pygame.K_LEFT) or Input.is_key_clicked(pygame.K_a):
            col = self.selected_index % self.GRID_COLS
            row = self.selected_index // self.GRID_COLS
            self.selected_index = row * self.GRID_COLS + ((col - 1) % self.GRID_COLS)
        elif Input.is_key_clicked(pygame.K_RIGHT) or Input.is_key_clicked(pygame.K_d):
            col = self.selected_index % self.GRID_COLS
            row = self.selected_index // self.GRID_COLS
            self.selected_index = row * self.GRID_COLS + ((col + 1) % self.GRID_COLS)
        elif Input.is_key_clicked(pygame.K_UP) or Input.is_key_clicked(pygame.K_w):
            col = self.selected_index % self.GRID_COLS
            row = self.selected_index // self.GRID_COLS
            self.selected_index = ((row - 1) % self.GRID_ROWS) * self.GRID_COLS + col
        elif Input.is_key_clicked(pygame.K_DOWN) or Input.is_key_clicked(pygame.K_s):
            col = self.selected_index % self.GRID_COLS
            row = self.selected_index // self.GRID_COLS
            self.selected_index = ((row + 1) % self.GRID_ROWS) * self.GRID_COLS + col
        elif Input.is_key_clicked(pygame.K_RETURN) or Input.is_key_clicked(pygame.K_SPACE):
            self._select_game(self.selected_index)
    def _select_game(self, index: int) -> None:
        if 0 <= index < len(self.games):
            selected_game = self.games[index]
            Logger.info(f"[MainMenuScene] Selected: {selected_game}")
            self.scene_manager.change_scene(GameModeScene(selected_game))
    def render(self) -> None:
        self.renderer.draw_text("MindWar Arena", (480, 45), size=54, color=(255, 255, 255))
        self.renderer.draw_text("Select a Game to Battle", (510, 115), size=24, color=(160, 180, 210))
        for index, game_name in enumerate(self.games):
            tx, ty, tw, th = self._get_tile_rect(index)
            is_active = (index == self.selected_index) or (index == self.hovered_index)
            if is_active:
                fill_color = (45, 70, 120)
                border_color = (110, 200, 255)
                text_color = (255, 255, 255)
            else:
                fill_color = (24, 28, 40)
                border_color = (55, 65, 85)
                text_color = (190, 200, 215)
            self.renderer.draw_filled_rectangle((tx, ty), (tw, th), fill_color)
            self.renderer.draw_rectangle((tx, ty), (tw, th), border_color)
            approx_text_width = len(game_name) * 13
            text_x = max(tx + 10, tx + (tw - approx_text_width) // 2)
            text_y = ty + (th - 30) // 2
            self.renderer.draw_text(game_name, (text_x, text_y), size=28, color=text_color)