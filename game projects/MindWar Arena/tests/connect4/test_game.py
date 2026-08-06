import unittest

from games.connect4.game import Connect4Game
from games.connect4.constants import (
    PLAYER_RED,
    PLAYER_YELLOW,
    GAME_RUNNING,
    GAME_OVER,
)


class DummyRenderer:
    def draw_grid(self, *args, **kwargs):
        pass

    def draw_circle(self, *args, **kwargs):
        pass

    def draw_filled_circle(self, *args, **kwargs):
        pass

    def draw_line(self, *args, **kwargs):
        pass

    def draw_rectangle(self, *args, **kwargs):
        pass

    def draw_filled_rectangle(self, *args, **kwargs):
        pass

    def draw_text(self, *args, **kwargs):
        pass

    def draw_overlay_message(self, *args, **kwargs):
        pass


class TestConnect4Game(unittest.TestCase):

    def setUp(self):
        self.game = Connect4Game(DummyRenderer())
        self.game.initialize()

    # ---------------------------------------------------------
    # Initialization
    # ---------------------------------------------------------

    def test_initialize(self):
        self.assertEqual(
            self.game.game_state,
            GAME_RUNNING,
        )

        self.assertEqual(
            self.game.move_count,
            0,
        )

    # ---------------------------------------------------------
    # Reset
    # ---------------------------------------------------------

    def test_reset(self):

        self.game.make_move(0)

        self.game.reset()

        self.assertEqual(
            self.game.move_count,
            0,
        )

        self.assertFalse(
            self.game.result.game_over
        )

    # ---------------------------------------------------------
    # Valid Move
    # ---------------------------------------------------------

    def test_make_move(self):

        success = self.game.make_move(0)

        self.assertTrue(success)

        self.assertEqual(
            self.game.move_count,
            1,
        )

    # ---------------------------------------------------------
    # Invalid Move
    # ---------------------------------------------------------

    def test_invalid_column(self):

        self.assertFalse(
            self.game.make_move(-1)
        )

        self.assertFalse(
            self.game.make_move(100)
        )

    # ---------------------------------------------------------
    # Switch Player
    # ---------------------------------------------------------

    def test_player_switch(self):

        first = self.game.current_player

        self.game.make_move(0)

        second = self.game.current_player

        self.assertNotEqual(
            first,
            second,
        )

    # ---------------------------------------------------------
    # Full Column
    # ---------------------------------------------------------

    def test_full_column(self):

        for _ in range(6):
            self.game.make_move(0)

        self.assertFalse(
            self.game.make_move(0)
        )

    # ---------------------------------------------------------
    # Horizontal Win
    # ---------------------------------------------------------

    def test_horizontal_win(self):

        self.game.make_move(0)   # R
        self.game.make_move(0)   # Y

        self.game.make_move(1)
        self.game.make_move(1)

        self.game.make_move(2)
        self.game.make_move(2)

        self.game.make_move(3)

        self.assertTrue(
            self.game.result.game_over
        )

        self.assertEqual(
            self.game.result.winner,
            PLAYER_RED,
        )

    # ---------------------------------------------------------
    # Game State
    # ---------------------------------------------------------

    def test_game_state(self):

        state = self.game.get_state()

        self.assertIn(
            "board",
            state,
        )

        self.assertIn(
            "current_player",
            state,
        )

        self.assertIn(
            "game_over",
            state,
        )

    # ---------------------------------------------------------
    # Game Over
    # ---------------------------------------------------------

    def test_is_game_over(self):

        self.assertFalse(
            self.game.is_game_over()
        )

        self.game.make_move(0)
        self.game.make_move(0)

        self.game.make_move(1)
        self.game.make_move(1)

        self.game.make_move(2)
        self.game.make_move(2)

        self.game.make_move(3)

        self.assertTrue(
            self.game.is_game_over()
        )

    # ---------------------------------------------------------
    # Winner
    # ---------------------------------------------------------

    def test_get_winner(self):

        self.game.make_move(0)
        self.game.make_move(0)

        self.game.make_move(1)
        self.game.make_move(1)

        self.game.make_move(2)
        self.game.make_move(2)

        self.game.make_move(3)

        self.assertEqual(
            self.game.get_winner(),
            PLAYER_RED,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)