import unittest

from games.connect4.board import Connect4Board
from games.connect4.rules import Connect4Rules
from games.connect4.constants import (
    BOARD_ROWS,
    BOARD_COLUMNS,
    PLAYER_RED,
    PLAYER_YELLOW,
    NO_WINNER,
)


class TestConnect4Rules(unittest.TestCase):

    def setUp(self):
        self.board = Connect4Board()

    # ---------------------------------------------------------
    # Horizontal Win
    # ---------------------------------------------------------

    def test_horizontal_win(self):
        for column in range(4):
            self.board.drop_piece(column, PLAYER_RED)

        self.assertEqual(
            Connect4Rules.check_winner(self.board),
            PLAYER_RED,
        )

    # ---------------------------------------------------------
    # Vertical Win
    # ---------------------------------------------------------

    def test_vertical_win(self):
        for _ in range(4):
            self.board.drop_piece(0, PLAYER_RED)

        self.assertEqual(
            Connect4Rules.check_winner(self.board),
            PLAYER_RED,
        )

    # ---------------------------------------------------------
    # Diagonal (\)
    # ---------------------------------------------------------

    def test_diagonal_right_win(self):

        # Column 0
        self.board.drop_piece(0, PLAYER_RED)

        # Column 1
        self.board.drop_piece(1, PLAYER_YELLOW)
        self.board.drop_piece(1, PLAYER_RED)

        # Column 2
        self.board.drop_piece(2, PLAYER_YELLOW)
        self.board.drop_piece(2, PLAYER_YELLOW)
        self.board.drop_piece(2, PLAYER_RED)

        # Column 3
        self.board.drop_piece(3, PLAYER_YELLOW)
        self.board.drop_piece(3, PLAYER_YELLOW)
        self.board.drop_piece(3, PLAYER_YELLOW)
        self.board.drop_piece(3, PLAYER_RED)

        self.assertEqual(
            Connect4Rules.check_winner(self.board),
            PLAYER_RED,
        )

    # ---------------------------------------------------------
    # Diagonal (/)
    # ---------------------------------------------------------

    def test_diagonal_left_win(self):

        # Column 3
        self.board.drop_piece(3, PLAYER_RED)

        # Column 2
        self.board.drop_piece(2, PLAYER_YELLOW)
        self.board.drop_piece(2, PLAYER_RED)

        # Column 1
        self.board.drop_piece(1, PLAYER_YELLOW)
        self.board.drop_piece(1, PLAYER_YELLOW)
        self.board.drop_piece(1, PLAYER_RED)

        # Column 0
        self.board.drop_piece(0, PLAYER_YELLOW)
        self.board.drop_piece(0, PLAYER_YELLOW)
        self.board.drop_piece(0, PLAYER_YELLOW)
        self.board.drop_piece(0, PLAYER_RED)

        self.assertEqual(
            Connect4Rules.check_winner(self.board),
            PLAYER_RED,
        )

    # ---------------------------------------------------------
    # No Winner
    # ---------------------------------------------------------

    def test_no_winner(self):

        self.board.drop_piece(0, PLAYER_RED)
        self.board.drop_piece(1, PLAYER_YELLOW)
        self.board.drop_piece(2, PLAYER_RED)

        self.assertEqual(
            Connect4Rules.check_winner(self.board),
            NO_WINNER,
        )

    # ---------------------------------------------------------
    # Game Over
    # ---------------------------------------------------------

    def test_game_over_on_win(self):

        for column in range(4):
            self.board.drop_piece(column, PLAYER_RED)

        self.assertTrue(
            Connect4Rules.is_game_over(self.board)
        )

    def test_game_not_over(self):

        self.board.drop_piece(0, PLAYER_RED)

        self.assertFalse(
            Connect4Rules.is_game_over(self.board)
        )

    # ---------------------------------------------------------
    # Winning Cells
    # ---------------------------------------------------------

    def test_winning_cells_horizontal(self):

        for column in range(4):
            self.board.drop_piece(column, PLAYER_RED)

        cells = Connect4Rules.get_winning_cells(
            self.board
        )

        self.assertEqual(len(cells), 4)

        expected = [
            (BOARD_ROWS - 1, 0),
            (BOARD_ROWS - 1, 1),
            (BOARD_ROWS - 1, 2),
            (BOARD_ROWS - 1, 3),
        ]

        self.assertEqual(cells, expected)

    # ---------------------------------------------------------
    # Evaluate Game
    # ---------------------------------------------------------

    def test_evaluate_game_win(self):

        for column in range(4):
            self.board.drop_piece(column, PLAYER_RED)

        result = Connect4Rules.evaluate_game(
            self.board
        )

        self.assertTrue(result.game_over)
        self.assertFalse(result.draw)
        self.assertEqual(
            result.winner,
            PLAYER_RED,
        )

    def test_evaluate_game_running(self):

        result = Connect4Rules.evaluate_game(
            self.board
        )

        self.assertFalse(result.game_over)
        self.assertFalse(result.draw)
        self.assertEqual(
            result.winner,
            None,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)