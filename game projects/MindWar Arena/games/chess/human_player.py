# games/chess/human_player.py
import pygame
from games.chess.constants import (PLAYER_BLACK,PLAYER_WHITE,)
class HumanPlayer:
    def __init__(self, board_renderer):
        self.board_renderer = board_renderer
        self.player = None
        self.selected_position = None
    def initialize(self):
        self.reset()
    def reset(self):
        self.selected_position = None
    def set_player(self, player):
        if player not in (PLAYER_WHITE,PLAYER_BLACK,):
            raise ValueError(f"Invalid player: {player}")
        self.player = player
        self.selected_position = None
    def get_action(self, game):
        if game is None:
            return None
        if game.is_game_over():
            return None
        current_player = (game.get_current_player())
        if self.player != current_player:
            self.set_player(current_player)
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            self.selected_position = None
            return None
        mouse_buttons = pygame.mouse.get_pressed()
        if not mouse_buttons[0]:
            return None
        mouse_position = pygame.mouse.get_pos()
        position = (self.board_renderer.screen_to_board(mouse_position))
        if position is None:
            return None
        if self.selected_position is None:
            if self._is_selectable_position(position,legal_moves,):
                self.selected_position = position
            return None
        if self._is_selectable_position(position,legal_moves,):
            self.selected_position = position
            return None
        selected_row, selected_column = (self.selected_position)
        move = (selected_row,selected_column,position[0],position[1],)
        if move in legal_moves:
            self.selected_position = None
            return move
        return None
    def clear_selection(self):
        self.selected_position = None
    def get_selected_position(self):
        return self.selected_position
    def _is_selectable_position(self,position,legal_moves,):
        row, column = position
        for move in legal_moves:
            if (move[0] == row and move[1] == column):
                return True
        return False