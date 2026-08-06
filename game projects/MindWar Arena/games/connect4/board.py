#games/connect4/board.py
from copy import deepcopy
from games.connect4.constants import (BOARD_ROWS,BOARD_COLUMNS,EMPTY,)
class Connect4Board:
    def __init__(self):
        self.reset()
    def reset(self):
        self._board = [[EMPTY for _ in range(BOARD_COLUMNS)]for _ in range(BOARD_ROWS)]
    def get_cell(self, row, column):
        return self._board[row][column]
    def set_cell(self, row, column, value):
        if not self.is_valid_position(row, column):
            return False
        self._board[row][column] = value
        return True
    def is_valid_position(self, row, column):
        return (0 <= row < BOARD_ROWS and 0 <= column < BOARD_COLUMNS)
    def is_column_full(self, column):
        if not (0 <= column < BOARD_COLUMNS):
            return True
        return self._board[0][column] != EMPTY
    def get_available_columns(self):
        columns = []
        for column in range(BOARD_COLUMNS):
            if not self.is_column_full(column):
                columns.append(column)
        return columns
    def get_next_open_row(self, column):
        if not (0 <= column < BOARD_COLUMNS):
            return None
        for row in range(BOARD_ROWS - 1, -1, -1):
            if self._board[row][column] == EMPTY:
                return row
        return None
    def drop_piece(self, column, player):
        row = self.get_next_open_row(column)
        if row is None:
            return None
        self._board[row][column] = player
        return row
    def is_board_full(self):
        return len(self.get_available_columns()) == 0
    def copy(self):
        board_copy = Connect4Board()
        board_copy._board = deepcopy(self._board)
        return board_copy
    def get_board_state(self):
        return deepcopy(self._board)
    def __str__(self):
        symbols = {EMPTY: ".",1: "R",2: "Y",}
        rows = []
        for row in self._board:
            rows.append(" ".join(symbols[cell] for cell in row))
        return "\n".join(rows)