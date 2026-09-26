# games/nine_mens_morris/board.py
from copy import deepcopy
from games.nine_mens_morris.constants import (BOARD_POSITIONS,EMPTY,PLAYER_BLACK,PLAYER_WHITE,PIECES_PER_PLAYER,)
class NineMensMorrisBoard:
    def __init__(self):
        self.reset()
    def reset(self):
        self._board = [EMPTY for _ in range(BOARD_POSITIONS)]
    def get_position(self, position):
        if not self.is_valid_position(position):
            return EMPTY
        return self._board[position]
    def set_position(self, position, value):
        if not self.is_valid_position(position):
            return False
        if value not in (EMPTY, PLAYER_BLACK, PLAYER_WHITE):
            return False
        self._board[position] = value
        return True
    def place_piece(self, position, player):
        if not self.is_valid_position(position):
            return False
        if player not in (PLAYER_BLACK, PLAYER_WHITE):
            return False
        if not self.is_position_empty(position):
            return False
        self._board[position] = player
        return True
    def remove_piece(self, position):
        if not self.is_valid_position(position):
            return False
        if self._board[position] == EMPTY:
            return False
        self._board[position] = EMPTY
        return True
    def move_piece(self, source, destination, player):
        if not self.is_valid_position(source):
            return False
        if not self.is_valid_position(destination):
            return False
        if player not in (PLAYER_BLACK, PLAYER_WHITE):
            return False
        if self._board[source] != player:
            return False
        if self._board[destination] != EMPTY:
            return False
        self._board[source] = EMPTY
        self._board[destination] = player
        return True
    def is_valid_position(self, position):
        return 0 <= position < BOARD_POSITIONS
    def is_position_empty(self, position):
        if not self.is_valid_position(position):
            return False
        return self._board[position] == EMPTY
    def get_available_positions(self):
        positions = []
        for position in range(BOARD_POSITIONS):
            if self._board[position] == EMPTY:
                positions.append(position)
        return positions
    def get_player_positions(self, player):
        if player not in (PLAYER_BLACK, PLAYER_WHITE):
            return []
        positions = []
        for position in range(BOARD_POSITIONS):
            if self._board[position] == player:
                positions.append(position)
        return positions
    def count_pieces(self, player):
        if player not in (PLAYER_BLACK, PLAYER_WHITE):
            return 0
        count = 0
        for position in range(BOARD_POSITIONS):
            if self._board[position] == player:
                count += 1
        return count
    def get_empty_count(self):
        count = 0
        for position in range(BOARD_POSITIONS):
            if self._board[position] == EMPTY:
                count += 1
        return count
    def is_board_full(self):
        return self.get_empty_count() == 0
    def has_minimum_pieces(self, player):
        return self.count_pieces(player) >= 3
    def get_board_state(self):
        return deepcopy(self._board)
    def copy(self):
        board_copy = NineMensMorrisBoard()
        board_copy._board = deepcopy(self._board)
        return board_copy
    def __str__(self):
        symbols = {EMPTY: ".",PLAYER_BLACK: "B",PLAYER_WHITE: "W",}
        return " ".join(symbols[position] for position in self._board)