"""
MindWar Arena
Phase 2 - Tic-Tac-Toe

Integration Tests

Verifies the complete interaction between:

- Game Controller
- Board
- Rules
- Human Player
- AI
- Restart System

This is the final verification of Phase 2.
"""

import unittest
from unittest.mock import patch

from games.tic_tac_toe.game import TicTacToeGame
from games.tic_tac_toe.constants import (
    PLAYER_X,
    PLAYER_O,
    EMPTY,
    GAME_RUNNING,
    GAME_OVER,
)


# ---------------------------------------------------------
# Fake Renderer
# ---------------------------------------------------------

class FakeRenderer:

    def draw_grid(self, **kwargs):
        pass

    def draw_cross(self, **kwargs):
        pass

    def draw_circle(self, **kwargs):
        pass

    def draw_line(self, **kwargs):
        pass

    def draw_overlay_message(self, **kwargs):
        pass


# ---------------------------------------------------------
# Integration Tests
# ---------------------------------------------------------

class TestIntegration(unittest.TestCase):

    def setUp(self):

        self.game = TicTacToeGame(
            FakeRenderer()
        )

        self.game.initialize()

    # -----------------------------------------------------

    def test_game_initializes(self):

        self.assertEqual(
            self.game.game_state,
            GAME_RUNNING,
        )

        self.assertFalse(
            self.game.is_game_over()
        )

    # -----------------------------------------------------

    def test_human_move(self):

        self.game.current_player = PLAYER_X

        self.assertTrue(
            self.game.make_move(0, 0)
        )

        self.assertEqual(
            self.game.board.get_cell(0, 0),
            PLAYER_X,
        )

    # -----------------------------------------------------

    def test_ai_move(self):

        self.game.current_player = PLAYER_O

        move = self.game.ai_player.get_action(
            self.game
        )

        self.assertIsNotNone(move)

        self.assertTrue(
            self.game.make_move(*move)
        )

    # -----------------------------------------------------

    def test_turn_switch(self):

        start = self.game.current_player

        self.game.make_move(0, 0)

        self.assertNotEqual(
            start,
            self.game.current_player,
        )

    # -----------------------------------------------------

    def test_illegal_move_rejected(self):

        self.game.make_move(0, 0)

        self.assertFalse(
            self.game.make_move(0, 0)
        )

    # -----------------------------------------------------

    def test_win_detection(self):

        self.game.current_player = PLAYER_X

        self.game.make_move(0, 0)

        self.game.current_player = PLAYER_X

        self.game.make_move(0, 1)

        self.game.current_player = PLAYER_X

        self.game.make_move(0, 2)

        self.assertTrue(
            self.game.is_game_over()
        )

        self.assertEqual(
            self.game.get_winner(),
            PLAYER_X,
        )

    # -----------------------------------------------------

    def test_draw_detection(self):

        board = self.game.board

        values = [

            [1,2,1],
            [1,2,2],
            [2,1,1],

        ]

        for r in range(3):
            for c in range(3):
                board.set_cell(
                    r,
                    c,
                    values[r][c],
                )

        self.game.result = self.game.result = \
            self.game.result = \
            self.game.result = \
            self.game.result = \
            self.game.result = \
            self.game.result = \
            self.game.result = \
            self.game.result = \
            self.game.result = \
            self.game.result = \
            self.game.result = \
            self.game.result = \
            self.game.result = \
            self.game.result = \
            self.game.result = \
            self.game.result = \
            self.game.result = \
            __import__(
                "games.tic_tac_toe.rules",
                fromlist=["TicTacToeRules"]
            ).TicTacToeRules.evaluate_game(board)

        self.assertTrue(
            self.game.result.draw
        )

    # -----------------------------------------------------

    def test_restart(self):

        self.game.make_move(0, 0)

        self.game.reset()

        self.assertEqual(
            self.game.move_count,
            0,
        )

        for row in range(3):
            for col in range(3):

                self.assertEqual(
                    self.game.board.get_cell(
                        row,
                        col,
                    ),
                    EMPTY,
                )

    # -----------------------------------------------------

    def test_starting_player_alternates(self):

        first = self.game.current_player

        self.game.reset()

        second = self.game.current_player

        self.assertNotEqual(
            first,
            second,
        )

    # -----------------------------------------------------

    def test_complete_game_runs_without_exception(self):

        try:

            self.game.make_move(0,0)
            self.game.make_move(1,1)
            self.game.make_move(0,1)
            self.game.make_move(2,2)
            self.game.make_move(0,2)

        except Exception as e:

            self.fail(str(e))


if __name__ == "__main__":
    unittest.main(verbosity=2)