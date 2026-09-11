# tests/test_checkers_game.py

import unittest

from games.checkers.ai import CheckersAI
from games.checkers.constants import (
    BLACK_KING,
    BLACK_MAN,
    EMPTY,
    GAME_MODE_HUMAN_VS_AI,
    GAME_MODE_HUMAN_VS_HUMAN,
    GAME_RUNNING,
    GAME_OVER,
    PLAYER_BLACK,
    PLAYER_WHITE,
    WHITE_MAN,
)
from games.checkers.game import CheckersGame


class TestCheckersGame(unittest.TestCase):

    def setUp(self):
        # The game controller itself does not require a real
        # renderer for the state-management tests below.
        self.game = CheckersGame(
            renderer=None,
            game_mode=GAME_MODE_HUMAN_VS_HUMAN,
        )

        self.game.initialize()

    def tearDown(self):
        self.game.shutdown()

    def clear_board(self):
        for row in range(8):
            for column in range(8):
                self.game.board.set_cell(
                    row,
                    column,
                    EMPTY,
                )

        self.game.result.reset()
        self.game.game_state = GAME_RUNNING
        self.game.in_multi_capture = False
        self.game.active_capture_piece = None
        self.game.move_count = 0

    def test_game_initializes(self):
        self.assertEqual(
            self.game.get_game_state(),
            GAME_RUNNING,
        )

        self.assertFalse(
            self.game.is_game_over()
        )

    def test_initial_piece_counts(self):
        self.assertEqual(
            self.game.get_black_count(),
            12,
        )

        self.assertEqual(
            self.game.get_white_count(),
            12,
        )

    def test_current_player_is_valid(self):
        self.assertIn(
            self.game.get_current_player(),
            (
                PLAYER_BLACK,
                PLAYER_WHITE,
            ),
        )

    def test_initial_move_count(self):
        self.assertEqual(
            self.game.move_count,
            0,
        )

    def test_make_valid_move(self):
        self.game.current_player = PLAYER_BLACK

        move = (
            2,
            1,
            3,
            0,
        )

        self.assertTrue(
            self.game.make_move(move)
        )

        self.assertEqual(
            self.game.move_count,
            1,
        )

        self.assertEqual(
            self.game.board.get_cell(2, 1),
            EMPTY,
        )

        self.assertEqual(
            self.game.board.get_cell(3, 0),
            BLACK_MAN,
        )

    def test_invalid_move_is_rejected(self):
        self.game.current_player = PLAYER_BLACK

        move = (
            2,
            1,
            2,
            2,
        )

        self.assertFalse(
            self.game.make_move(move)
        )

        self.assertEqual(
            self.game.move_count,
            0,
        )

    def test_turn_switches_after_normal_move(self):
        self.game.current_player = PLAYER_BLACK

        move = (
            2,
            1,
            3,
            0,
        )

        self.assertTrue(
            self.game.make_move(move)
        )

        self.assertEqual(
            self.game.current_player,
            PLAYER_WHITE,
        )

    def test_multi_capture_starts(self):
        self.clear_board()

        self.game.current_player = PLAYER_BLACK

        self.game.board.set_cell(
            2,
            1,
            BLACK_MAN,
        )

        self.game.board.set_cell(
            3,
            2,
            WHITE_MAN,
        )

        self.game.board.set_cell(
            5,
            4,
            WHITE_MAN,
        )

        first_move = (
            2,
            1,
            4,
            3,
        )

        self.assertTrue(
            self.game.make_move(first_move)
        )

        self.assertTrue(
            self.game.is_in_multi_capture()
        )

        self.assertEqual(
            self.game.get_active_capture_piece(),
            (4, 3),
        )

        self.assertEqual(
            self.game.current_player,
            PLAYER_BLACK,
        )

    def test_multi_capture_second_move(self):
        self.clear_board()

        self.game.current_player = PLAYER_BLACK

        self.game.board.set_cell(
            2,
            1,
            BLACK_MAN,
        )

        self.game.board.set_cell(
            3,
            2,
            WHITE_MAN,
        )

        self.game.board.set_cell(
            5,
            4,
            WHITE_MAN,
        )

        first_move = (
            2,
            1,
            4,
            3,
        )

        self.assertTrue(
            self.game.make_move(first_move)
        )

        second_move = (
            4,
            3,
            6,
            5,
        )

        self.assertTrue(
            self.game.make_move(second_move)
        )

        self.assertFalse(
            self.game.is_in_multi_capture()
        )

        self.assertIsNone(
            self.game.get_active_capture_piece()
        )

        self.assertEqual(
            self.game.current_player,
            PLAYER_WHITE,
        )

        self.assertEqual(
            self.game.board.get_cell(6, 5),
            BLACK_MAN,
        )

    def test_multi_capture_cannot_be_interrupted_by_another_piece(self):
        self.clear_board()

        self.game.current_player = PLAYER_BLACK

        self.game.board.set_cell(
            2,
            1,
            BLACK_MAN,
        )

        self.game.board.set_cell(
            3,
            2,
            WHITE_MAN,
        )

        self.game.board.set_cell(
            5,
            4,
            WHITE_MAN,
        )

        self.game.board.set_cell(
            2,
            5,
            BLACK_MAN,
        )

        first_move = (
            2,
            1,
            4,
            3,
        )

        self.assertTrue(
            self.game.make_move(first_move)
        )

        interrupted_move = (
            2,
            5,
            3,
            4,
        )

        self.assertFalse(
            self.game.make_move(
                interrupted_move
            )
        )

        self.assertTrue(
            self.game.is_in_multi_capture()
        )

        self.assertEqual(
            self.game.get_active_capture_piece(),
            (4, 3),
        )

    def test_multi_capture_must_continue_from_active_piece(self):
        self.clear_board()

        self.game.current_player = PLAYER_BLACK

        self.game.board.set_cell(
            2,
            1,
            BLACK_MAN,
        )

        self.game.board.set_cell(
            3,
            2,
            WHITE_MAN,
        )

        self.game.board.set_cell(
            5,
            4,
            WHITE_MAN,
        )

        first_move = (
            2,
            1,
            4,
            3,
        )

        self.assertTrue(
            self.game.make_move(first_move)
        )

        wrong_source = (
            2,
            1,
            4,
            3,
        )

        self.assertFalse(
            self.game.make_move(
                wrong_source
            )
        )

    def test_capture_removes_piece_and_updates_count(self):
        self.clear_board()

        self.game.current_player = PLAYER_BLACK

        self.game.board.set_cell(
            2,
            1,
            BLACK_MAN,
        )

        self.game.board.set_cell(
            3,
            2,
            WHITE_MAN,
        )

        self.assertEqual(
            self.game.get_white_count(),
            1,
        )

        move = (
            2,
            1,
            4,
            3,
        )

        self.assertTrue(
            self.game.make_move(move)
        )

        self.assertEqual(
            self.game.get_white_count(),
            0,
        )

    def test_winning_by_capturing_last_piece(self):
        self.clear_board()

        self.game.current_player = PLAYER_BLACK

        self.game.board.set_cell(
            2,
            1,
            BLACK_MAN,
        )

        self.game.board.set_cell(
            3,
            2,
            WHITE_MAN,
        )

        move = (
            2,
            1,
            4,
            3,
        )

        self.assertTrue(
            self.game.make_move(move)
        )

        self.assertTrue(
            self.game.is_game_over()
        )

        self.assertEqual(
            self.game.get_winner(),
            PLAYER_BLACK,
        )

        self.assertEqual(
            self.game.get_game_state(),
            GAME_OVER,
        )

    def test_get_state_contains_required_fields(self):
        state = self.game.get_state()

        required_fields = {
            "board",
            "current_player",
            "winner",
            "game_state",
            "game_over",
            "draw",
            "move_count",
            "in_multi_capture",
            "active_capture_piece",
            "legal_moves",
            "black_count",
            "white_count",
        }

        self.assertTrue(
            required_fields.issubset(
                state.keys()
            )
        )

    def test_get_state_board_is_independent_copy(self):
        state = self.game.get_state()

        state["board"][0][1] = BLACK_KING

        self.assertNotEqual(
            self.game.board.get_cell(0, 1),
            BLACK_KING,
        )

    def test_reset_restores_board(self):
        self.game.current_player = PLAYER_BLACK

        move = (
            2,
            1,
            3,
            0,
        )

        self.assertTrue(
            self.game.make_move(move)
        )

        self.game.reset()

        self.assertEqual(
            self.game.get_black_count(),
            12,
        )

        self.assertEqual(
            self.game.get_white_count(),
            12,
        )

        self.assertEqual(
            self.game.move_count,
            0,
        )

        self.assertFalse(
            self.game.is_game_over()
        )

        self.assertFalse(
            self.game.is_in_multi_capture()
        )

        self.assertIsNone(
            self.game.get_active_capture_piece()
        )

    def test_human_vs_ai_mode(self):
        game = CheckersGame(
            renderer=None,
            game_mode=GAME_MODE_HUMAN_VS_AI,
        )

        game.initialize()

        self.assertIsNotNone(
            game.ai
        )

        game.shutdown()

    def test_ai_returns_legal_move(self):
        game = CheckersGame(
            renderer=None,
            game_mode=GAME_MODE_HUMAN_VS_AI,
        )

        game.initialize()

        game.current_player = PLAYER_BLACK

        legal_moves = game.get_legal_moves()

        action = game.ai.get_action(game)

        self.assertIsNotNone(action)

        self.assertIn(
            action,
            legal_moves,
        )

        game.shutdown()

    def test_ai_move_has_correct_format(self):
        game = CheckersGame(
            renderer=None,
            game_mode=GAME_MODE_HUMAN_VS_AI,
        )

        game.initialize()

        action = game.ai.get_action(game)

        self.assertIsInstance(
            action,
            tuple,
        )

        self.assertEqual(
            len(action),
            4,
        )

        for value in action:
            self.assertIsInstance(
                value,
                int,
            )

        game.shutdown()

    def test_ai_select_action_from_state(self):
        game = CheckersGame(
            renderer=None,
            game_mode=GAME_MODE_HUMAN_VS_AI,
        )

        game.initialize()

        state = game.get_state()

        action = game.ai.select_action(
            state
        )

        self.assertIsNotNone(action)

        self.assertIn(
            action,
            state["legal_moves"],
        )

        game.shutdown()

    def test_ai_player_assignment(self):
        ai = CheckersAI(
            PLAYER_BLACK
        )

        self.assertEqual(
            ai.player,
            PLAYER_BLACK,
        )

        ai.set_player(
            PLAYER_WHITE
        )

        self.assertEqual(
            ai.player,
            PLAYER_WHITE,
        )


if __name__ == "__main__":
    unittest.main()