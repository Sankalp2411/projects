# games/pente/board.py
from copy import deepcopy
from games.pente.constants import (BOARD_ROWS,BOARD_COLUMNS,EMPTY,PLAYER_BLACK,PLAYER_WHITE,)
class PenteBoard:
    def __init__(self):
        self.reset()
    def reset(self):
        self._board = [[EMPTY for _ in range(BOARD_COLUMNS)] for _ in range(BOARD_ROWS)]
    def get_cell(self, row, column):
        return self._board[row][column]
    def set_cell(self, row, column, value):
        if not self.is_valid_position(row, column):
            return False
        if value not in (EMPTY, PLAYER_BLACK, PLAYER_WHITE):
            return False
        self._board[row][column] = value
        return True
    def place_stone(self, row, column, player):
        if not self.is_valid_position(row, column):
            return False
        if player not in (PLAYER_BLACK, PLAYER_WHITE):
            return False
        if not self.is_cell_empty(row, column):
            return False
        self._board[row][column] = player
        return True
    def remove_stone(self, row, column):
        if not self.is_valid_position(row, column):
            return False
        if self._board[row][column] == EMPTY:
            return False
        self._board[row][column] = EMPTY
        return True
    def is_valid_position(self, row, column):
        return (0 <= row < BOARD_ROWS and 0 <= column < BOARD_COLUMNS)
    def is_cell_empty(self, row, column):
        if not self.is_valid_position(row, column):
            return False
        return self._board[row][column] == EMPTY
    def is_board_full(self):
        for row in self._board:
            for cell in row:
                if cell == EMPTY:
                    return False
        return True
    def get_available_moves(self):
        moves = []
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                if self._board[row][column] == EMPTY:
                    moves.append((row, column))
        return moves
    def count_stones(self, player):
        if player not in (PLAYER_BLACK, PLAYER_WHITE):
            return 0
        count = 0
        for row in self._board:
            for cell in row:
                if cell == player:
                    count += 1
        return count
    def get_empty_count(self):
        count = 0
        for row in self._board:
            for cell in row:
                if cell == EMPTY:
                    count += 1
        return count
    def copy(self):
        board_copy = PenteBoard()
        board_copy._board = deepcopy(self._board)
        return board_copy
    def get_board_state(self):
        return deepcopy(self._board)
    def __str__(self):
        symbols = {EMPTY: ".",PLAYER_BLACK: "B",PLAYER_WHITE: "W",}
        rows = []
        for row in self._board:
            rows.append(" ".join(symbols[cell] for cell in row))
        return "\n".join(rows)