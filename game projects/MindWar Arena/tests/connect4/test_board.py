import unittest

from games.connect4.board import Connect4Board
from games.connect4.constants import (
    BOARD_ROWS,
    BOARD_COLUMNS,
    EMPTY,
    PLAYER_RED,
    PLAYER_YELLOW,
)


class TestConnect4Board(unittest.TestCase):

    def setUp(self):
        self.board = Connect4Board()

    # ---------------------------------------------------------
    # Initialization
    # ---------------------------------------------------------

    def test_board_dimensions(self):
        state = self.board.get_board_state()

        self.assertEqual(len(state), BOARD_ROWS)
        self.assertEqual(len(state[0]), BOARD_COLUMNS)

    def test_board_starts_empty(self):
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                self.assertEqual(
                    self.board.get_cell(row, column),
                    EMPTY
                )

    # ---------------------------------------------------------
    # Reset
    # ---------------------------------------------------------

    def test_reset(self):
        self.board.drop_piece(0, PLAYER_RED)
        self.board.drop_piece(1, PLAYER_YELLOW)

        self.board.reset()

        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                self.assertEqual(
                    self.board.get_cell(row, column),
                    EMPTY
                )

    # ---------------------------------------------------------
    # Drop Piece
    # ---------------------------------------------------------

    def test_drop_piece_bottom(self):
        row = self.board.drop_piece(
            3,
            PLAYER_RED,
        )

        self.assertEqual(row, BOARD_ROWS - 1)
        self.assertEqual(
            self.board.get_cell(BOARD_ROWS - 1, 3),
            PLAYER_RED,
        )

    def test_drop_piece_stacking(self):
        row1 = self.board.drop_piece(
            2,
            PLAYER_RED,
        )

        row2 = self.board.drop_piece(
            2,
            PLAYER_YELLOW,
        )

        self.assertEqual(row1, BOARD_ROWS - 1)
        self.assertEqual(row2, BOARD_ROWS - 2)

        self.assertEqual(
            self.board.get_cell(BOARD_ROWS - 1, 2),
            PLAYER_RED,
        )

        self.assertEqual(
            self.board.get_cell(BOARD_ROWS - 2, 2),
            PLAYER_YELLOW,
        )

    # ---------------------------------------------------------
    # Column Validation
    # ---------------------------------------------------------

    def test_invalid_column_negative(self):
        row = self.board.drop_piece(
            -1,
            PLAYER_RED,
        )

        self.assertIsNone(row)

    def test_invalid_column_large(self):
        row = self.board.drop_piece(
            BOARD_COLUMNS,
            PLAYER_RED,
        )

        self.assertIsNone(row)

    def test_full_column(self):

        for _ in range(BOARD_ROWS):
            self.board.drop_piece(
                0,
                PLAYER_RED,
            )

        row = self.board.drop_piece(
            0,
            PLAYER_RED,
        )

        self.assertIsNone(row)

    # ---------------------------------------------------------
    # Available Moves
    # ---------------------------------------------------------

    def test_available_moves_initial(self):
        moves = self.board.get_available_columns()

        self.assertEqual(
            len(moves),
            BOARD_COLUMNS,
        )

    def test_available_moves_after_full_column(self):

        for _ in range(BOARD_ROWS):
            self.board.drop_piece(
                0,
                PLAYER_RED,
            )

        moves = self.board.get_available_columns()

        self.assertNotIn(0, moves)

        self.assertEqual(
            len(moves),
            BOARD_COLUMNS - 1,
        )

    # ---------------------------------------------------------
    # Board Full
    # ---------------------------------------------------------

    def test_board_not_full(self):
        self.assertFalse(
            self.board.is_board_full()
        )

    def test_board_full(self):

        player = PLAYER_RED

        for column in range(BOARD_COLUMNS):
            for _ in range(BOARD_ROWS):

                self.board.drop_piece(
                    column,
                    player,
                )

                player = (
                    PLAYER_YELLOW
                    if player == PLAYER_RED
                    else PLAYER_RED
                )

        self.assertTrue(
            self.board.is_board_full()
        )

    # ---------------------------------------------------------
    # Copy
    # ---------------------------------------------------------

    def test_copy(self):

        self.board.drop_piece(
            3,
            PLAYER_RED,
        )

        copied = self.board.copy()

        self.assertEqual(
            copied.get_board_state(),
            self.board.get_board_state(),
        )

        copied.drop_piece(
            4,
            PLAYER_YELLOW,
        )

        self.assertNotEqual(
            copied.get_board_state(),
            self.board.get_board_state(),
        )

    # ---------------------------------------------------------
    # Board State
    # ---------------------------------------------------------

    def test_get_board_state(self):

        state = self.board.get_board_state()

        self.assertEqual(
            len(state),
            BOARD_ROWS,
        )

        self.assertEqual(
            len(state[0]),
            BOARD_COLUMNS,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)