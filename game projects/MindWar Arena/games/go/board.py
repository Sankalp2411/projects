#games/go/board.py
from copy import deepcopy
from games.go.constants import (BOARD_COLUMNS,BOARD_ROWS,EMPTY,PLAYER_BLACK,PLAYER_WHITE,)
class GoBoard:
    def __init__(self):
        self._board = []
        self.reset()
    def reset(self):
        self._board = [[EMPTY for _ in range(BOARD_COLUMNS)] for _ in range(BOARD_ROWS)]
    def is_valid_position(self, row, column):
        return ( 0 <= row < BOARD_ROWS and 0 <= column < BOARD_COLUMNS)
    def get_cell(self, row, column):
        if not self.is_valid_position(row, column):
            raise ValueError(f"Invalid board position: ({row}, {column})")
        return self._board[row][column]
    def set_cell(self, row, column, value):
        if not self.is_valid_position(row, column):
            raise ValueError(f"Invalid board position: ({row}, {column})")
        if value not in (EMPTY,PLAYER_BLACK,PLAYER_WHITE,):
            raise ValueError(f"Invalid cell value: {value}")
        self._board[row][column] = value
    def place_stone(self, row, column, player):
        if not self.is_valid_position(row, column):
            return False
        if player not in (PLAYER_BLACK,PLAYER_WHITE,):
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
    def is_cell_empty(self, row, column):
        if not self.is_valid_position(row, column):
            return False
        return self._board[row][column] == EMPTY
    def get_empty_positions(self):
        positions = []
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                if self._board[row][column] == EMPTY:
                    positions.append((row, column))
        return positions
    def get_player_positions(self, player):
        if player not in (PLAYER_BLACK,PLAYER_WHITE,):
            return []
        positions = []
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                if self._board[row][column] == player:
                    positions.append((row, column))
        return positions
    def count_stones(self, player):
        if player not in (PLAYER_BLACK,PLAYER_WHITE,):
            return 0
        count = 0
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                if self._board[row][column] == player:
                    count += 1
        return count
    def get_empty_count(self):
        count = 0
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                if self._board[row][column] == EMPTY:
                    count += 1
        return count
    def is_board_full(self):
        return self.get_empty_count() == 0
    def get_board_state(self):
        return deepcopy(self._board)
    def set_board_state(self, board_state):
        if not isinstance(board_state, list):
            raise ValueError("Invalid board state.")
        if len(board_state) != BOARD_ROWS:
            raise ValueError("Invalid board state.")
        for row in board_state:
            if not isinstance(row, list):
                raise ValueError("Invalid board state.")
            if len(row) != BOARD_COLUMNS:
                raise ValueError("Invalid board state.")
            for value in row:
                if value not in (EMPTY,PLAYER_BLACK,PLAYER_WHITE,):
                    raise ValueError("Invalid board value.")
        self._board = deepcopy(board_state)
    def copy(self):
        new_board = GoBoard()
        new_board._board = deepcopy(self._board)
        return new_board
    def __str__(self):
        symbols = {EMPTY: ".",PLAYER_BLACK: "B",PLAYER_WHITE: "W",}
        rows = []
        for row in self._board:
            rows.append(" ".join(symbols[cell] for cell in row))
        return "\n".join(rows)