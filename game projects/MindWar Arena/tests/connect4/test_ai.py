import unittest

from games.connect4.ai import Connect4AI
from games.connect4.board import Connect4Board
from games.connect4.constants import (
    BOARD_COLUMNS,
    BOARD_ROWS,
    PLAYER_RED,
)


class TestConnect4AI(unittest.TestCase):

    def setUp(self):
        self.ai = Connect4AI()
        self.ai.initialize()

        self.board = Connect4Board()

    # ---------------------------------------------------------
    # Initialization
    # ---------------------------------------------------------

    def test_initialize(self):
        self.assertTrue(self.ai.initialized)

    # ---------------------------------------------------------
    # Random Move
    # ---------------------------------------------------------

    def test_random_move_is_valid(self):
        state = {
            "board": self.board.get_board_state(),
        }

        move = self.ai.select_action(state)

        self.assertIsNotNone(move)
        self.assertGreaterEqual(move, 0)
        self.assertLess(move, BOARD_COLUMNS)

    # ---------------------------------------------------------
    # Full Column
    # ---------------------------------------------------------

    def test_ai_never_selects_full_column(self):

        for _ in range(BOARD_ROWS):
            self.board.drop_piece(0, PLAYER_RED)

        state = {
            "board": self.board.get_board_state(),
        }

        for _ in range(100):

            move = self.ai.select_action(state)

            self.assertNotEqual(move, 0)

    # ---------------------------------------------------------
    # No Available Moves
    # ---------------------------------------------------------

    def test_no_available_moves(self):

        player = PLAYER_RED

        for column in range(BOARD_COLUMNS):
            for _ in range(BOARD_ROWS):

                self.board.drop_piece(column, player)

                player = (
                    2 if player == 1 else 1
                )

        state = {
            "board": self.board.get_board_state(),
        }

        move = self.ai.select_action(state)

        self.assertIsNone(move)

    # ---------------------------------------------------------
    # Reset
    # ---------------------------------------------------------

    def test_reset(self):
        self.ai.reset()

        self.assertFalse(self.ai.initialized)


if __name__ == "__main__":
    unittest.main(verbosity=2)