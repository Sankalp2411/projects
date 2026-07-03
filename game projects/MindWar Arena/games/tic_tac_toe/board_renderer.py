"""
MindWar Arena
Phase 2 - Tic-Tac-Toe

board_renderer.py

Responsible only for rendering the Tic-Tac-Toe board.

Responsibilities
----------------
• Draw board grid
• Draw X symbols
• Draw O symbols
• Render current board state

This class NEVER modifies the game state.
It only visualizes it.
"""

from games.tic_tac_toe.constants import (
    BOARD_ROWS,
    BOARD_COLUMNS,
    CELL_SIZE,
    BOARD_PADDING,
    GRID_COLOR,
    X_COLOR,
    O_COLOR,
    EMPTY,
    PLAYER_X,
    PLAYER_O,
)


class BoardRenderer:

    def __init__(self, renderer):

        self.renderer = renderer

        self.origin_x = BOARD_PADDING
        self.origin_y = BOARD_PADDING

    # ---------------------------------------------------------
    # Public Rendering
    # ---------------------------------------------------------

    def render(self, board):

        self.draw_grid()

        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):

                value = board.get_cell(row, column)

                if value == PLAYER_X:
                    self.draw_x(row, column)

                elif value == PLAYER_O:
                    self.draw_o(row, column)

    # ---------------------------------------------------------
    # Grid
    # ---------------------------------------------------------

    def draw_grid(self):

        self.renderer.draw_grid(
            origin=(self.origin_x, self.origin_y),
            rows=BOARD_ROWS,
            columns=BOARD_COLUMNS,
            cell_size=CELL_SIZE,
            color=GRID_COLOR,
        )

    # ---------------------------------------------------------
    # X
    # ---------------------------------------------------------

    def draw_x(self, row, column):

        center = self.get_cell_center(row, column)

        self.renderer.draw_cross(
            center=center,
            size=CELL_SIZE * 0.60,
            color=X_COLOR,
        )

    # ---------------------------------------------------------
    # O
    # ---------------------------------------------------------

    def draw_o(self, row, column):

        center = self.get_cell_center(row, column)

        self.renderer.draw_circle(
            center=center,
            radius=CELL_SIZE * 0.30,
            color=O_COLOR,
        )

    # ---------------------------------------------------------
    # Utility
    # ---------------------------------------------------------

    def get_cell_center(self, row, column):

        x = (
            self.origin_x
            + column * CELL_SIZE
            + CELL_SIZE / 2
        )

        y = (
            self.origin_y
            + row * CELL_SIZE
            + CELL_SIZE / 2
        )

        return (x, y)