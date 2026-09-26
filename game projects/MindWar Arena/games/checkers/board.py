# games/checkers/board.py
from copy import deepcopy
from games.checkers.constants import (BOARD_COLUMNS,BOARD_ROWS,BLACK_KING,BLACK_MAN,EMPTY,PLAYER_BLACK,PLAYER_WHITE,WHITE_KING,WHITE_MAN,)
class CheckersBoard:
    def __init__(self):
        self._board = []
        self.reset()
    def reset(self):
        self._board = [[EMPTY for _ in range(BOARD_COLUMNS)] for _ in range(BOARD_ROWS)]
        for row in range(3):
            for column in range(BOARD_COLUMNS):
                if self.is_dark_square(row, column):
                    self._board[row][column] = BLACK_MAN
        for row in range(BOARD_ROWS - 3, BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                if self.is_dark_square(row, column):
                    self._board[row][column] = WHITE_MAN
    def get_cell(self, row, column):
        if not self.is_valid_position(row, column):
            raise ValueError(f"Invalid board position: ({row}, {column})")
        return self._board[row][column]
    def set_cell(self, row, column, value):
        if not self.is_valid_position(row, column):
            raise ValueError(f"Invalid board position: ({row}, {column})")
        if value not in (EMPTY,BLACK_MAN,BLACK_KING,WHITE_MAN,WHITE_KING,):
            raise ValueError(f"Invalid piece value: {value}")
        self._board[row][column] = value
    def is_valid_position(self, row, column):
        return (0 <= row < BOARD_ROWS and 0 <= column < BOARD_COLUMNS)
    def is_dark_square(self, row, column):
        if not self.is_valid_position(row, column):
            raise ValueError(f"Invalid board position: ({row}, {column})")
        return (row + column) % 2 == 1
    def is_playable_square(self, row, column):
        return self.is_dark_square(row, column)
    def is_cell_empty(self, row, column):
        return self.get_cell(row, column) == EMPTY
    def count_pieces(self, player):
        if player == PLAYER_BLACK:
            pieces = (BLACK_MAN, BLACK_KING)
        elif player == PLAYER_WHITE:
            pieces = (WHITE_MAN, WHITE_KING)
        else:
            raise ValueError(f"Invalid player: {player}")
        count = 0
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                if self._board[row][column] in pieces:
                    count += 1
        return count
    def get_piece_positions(self, player):
        if player == PLAYER_BLACK:
            pieces = (BLACK_MAN, BLACK_KING)
        elif player == PLAYER_WHITE:
            pieces = (WHITE_MAN, WHITE_KING)
        else:
            raise ValueError(f"Invalid player: {player}")
        positions = []
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                if self._board[row][column] in pieces:
                    positions.append((row, column))
        return positions
    def get_board_state(self):
        return deepcopy(self._board)
    def copy(self):
        new_board = CheckersBoard()
        new_board._board = deepcopy(self._board)
        return new_board
    def __str__(self):
        symbols = {EMPTY: ".",BLACK_MAN: "b",BLACK_KING: "B",WHITE_MAN: "w",WHITE_KING: "W",}
        rows = []
        for row in self._board:
            rows.append(" ".join(symbols[cell] for cell in row))
        return "\n".join(rows)