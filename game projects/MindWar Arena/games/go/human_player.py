#games/go/human_player.py
import pygame
from engine.core.input import Input
from games.go.constants import (ACTION_PASS,PLAYER_BLACK,PLAYER_WHITE,)
class HumanPlayer:
    def __init__(self, board_renderer):
        self.board_renderer = board_renderer
        self.player = None
    def initialize(self):
        self.reset()
    def reset(self):
        self.player = None
    def set_player(self, player):
        if player not in (PLAYER_BLACK,PLAYER_WHITE,):
            raise ValueError(f"Invalid player: {player}")
        self.player = player
    def get_action(self, game):
        if game is None:
            return None
        if game.is_game_over():
            return None
        current_player = game.get_current_player()
        if self.player != current_player:
            self.set_player(current_player)
        if Input.is_left_mouse_clicked():
            mouse_x, mouse_y = (Input.get_mouse_position())
            position = (self.board_renderer.screen_to_board((mouse_x, mouse_y)))
            if position is not None:
                return position
        keyboard = pygame.key.get_pressed()
        if keyboard[pygame.K_p]:
            return ACTION_PASS
        return None