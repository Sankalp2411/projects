# games/othello/board.py
from copy import deepcopy
from games.othello.constants import (BOARD_ROWS,BOARD_COLUMNS,EMPTY,PLAYER_BLACK,PLAYER_WHITE,)
class OthelloBoard:
    def __init__(self):
        self._board = []
        self.reset()
    def reset(self):
        self._board = [[EMPTY for _ in range(BOARD_COLUMNS)] for _ in range(BOARD_ROWS)]
        middle_row = BOARD_ROWS // 2
        middle_column = BOARD_COLUMNS // 2
        self._board[middle_row - 1][middle_column - 1] = PLAYER_WHITE
        self._board[middle_row - 1][middle_column] = PLAYER_BLACK
        self._board[middle_row][middle_column - 1] = PLAYER_BLACK
        self._board[middle_row][middle_column] = PLAYER_WHITE
    def get_cell(self, row, column):
        if not self.is_valid_position(row, column):
            raise ValueError(f"Invalid board position: ({row}, {column})")
        return self._board[row][column]
    def set_cell(self, row, column, value):
        if not self.is_valid_position(row, column):
            raise ValueError(f"Invalid board position: ({row}, {column})")
        if value not in (EMPTY, PLAYER_BLACK, PLAYER_WHITE):
            raise ValueError(f"Invalid cell value: {value}")
        self._board[row][column] = value
    def is_valid_position(self, row, column):
        return (0 <= row < BOARD_ROWS and 0 <= column < BOARD_COLUMNS)
    def is_cell_empty(self, row, column):
        return self.get_cell(row, column) == EMPTY
    def is_board_full(self):
        return self.get_empty_count() == 0
    def get_available_moves(self):
        moves = []
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                if self._board[row][column] == EMPTY:
                    moves.append((row, column))
        return moves
    def get_empty_count(self):
        count = 0
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                if self._board[row][column] == EMPTY:
                    count += 1
        return count
    def count_stones(self, player):
        if player not in (PLAYER_BLACK, PLAYER_WHITE):
            raise ValueError(f"Invalid player: {player}")
        count = 0
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                if self._board[row][column] == player:
                    count += 1
        return count
    def copy(self):
        new_board = OthelloBoard()
        new_board._board = deepcopy(self._board)
        return new_board
    def get_board_state(self):
        return deepcopy(self._board)
    def __str__(self):
        symbols = {EMPTY: ".",PLAYER_BLACK: "B",PLAYER_WHITE: "W",}
        rows = []
        for row in self._board:
            rows.append(" ".join(symbols[cell] for cell in row))
        return "\n".join(rows)