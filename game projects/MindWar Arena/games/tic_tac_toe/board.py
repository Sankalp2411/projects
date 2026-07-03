"""
MindWar Arena
Phase 2 - Tic-Tac-Toe

board.py

This module implements the Tic-Tac-Toe board.

Responsibilities:
- Store the board state.
- Manage cell values.
- Provide board utility functions.

This module does NOT:
- Check game rules.
- Detect winners.
- Handle turns.
- Control AI.
- Render graphics.
"""

from copy import deepcopy

from games.tic_tac_toe.constants import (
    BOARD_ROWS,
    BOARD_COLUMNS,
    EMPTY,
)


class TicTacToeBoard:
    """
    Represents the Tic-Tac-Toe board.

    The board is responsible only for storing and managing
    board data.
    """

    def __init__(self):
        self.reset()

    def reset(self):
        """
        Reset the board to its initial empty state.
        """
        self._board = [
            [EMPTY for _ in range(BOARD_COLUMNS)]
            for _ in range(BOARD_ROWS)
        ]

    def get_cell(self, row, column):
        """
        Return the value stored at the given position.

        Returns:
            int: Cell value.
        """
        return self._board[row][column]

    def set_cell(self, row, column, value):
        """
        Set a value at the specified board position.

        Returns:
            bool:
                True  -> success
                False -> invalid position
        """
        if not self.is_valid_position(row, column):
            return False

        self._board[row][column] = value
        return True

    def is_cell_empty(self, row, column):
        """
        Check whether a cell is empty.
        """
        if not self.is_valid_position(row, column):
            return False

        return self._board[row][column] == EMPTY

    def is_board_full(self):
        """
        Return True if no empty cells remain.
        """
        for row in self._board:
            for cell in row:
                if cell == EMPTY:
                    return False

        return True

    def get_available_moves(self):
        """
        Return every empty board position.

        Returns:
            list[tuple[int, int]]
        """
        moves = []

        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                if self._board[row][column] == EMPTY:
                    moves.append((row, column))

        return moves

    def is_valid_position(self, row, column):
        """
        Check whether coordinates are inside the board.
        """
        return (
            0 <= row < BOARD_ROWS
            and
            0 <= column < BOARD_COLUMNS
        )

    def copy(self):
        """
        Return a deep copy of this board.
        """
        board_copy = TicTacToeBoard()
        board_copy._board = deepcopy(self._board)
        return board_copy

    def get_board_state(self):
        """
        Return a deep copy of the board state.
        """
        return deepcopy(self._board)

    def __str__(self):
        """
        Return a human-readable board representation.
        """

        symbols = {
            EMPTY: ".",
            1: "X",
            2: "O",
        }

        rows = []

        for row in self._board:
            rows.append(
                " ".join(symbols[cell] for cell in row)
            )

        return "\n".join(rows)