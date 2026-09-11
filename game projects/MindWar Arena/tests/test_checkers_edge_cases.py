# tests/test_checkers_edge_cases.py

import unittest

from games.checkers.constants import (
    BLACK_KING,
    BLACK_MAN,
    EMPTY,
    GAME_OVER,
    GAME_RUNNING,
    PLAYER_BLACK,
    PLAYER_WHITE,
    WHITE_KING,
    WHITE_MAN,
)
from games.checkers.game import CheckersGame
from games.checkers.rules import CheckersRules


class TestCheckersEdgeCases(unittest.TestCase):

    def setUp(self):
        self.game = CheckersGame(
            renderer=None
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

    # --------------------------------------------------
    # KING CAPTURE TESTS
    # --------------------------------------------------

    def test_black_king_can_capture_backward(self):
        self.clear_board()

        board = self.game.board

        board.set_cell(
            4,
            3,
            BLACK_KING,
        )

        board.set_cell(
            3,
            2,
            WHITE_MAN,
        )

        move = (
            4,
            3,
            2,
            1,
        )

        self.assertTrue(
            CheckersRules.is_valid_move(
                board,
                move,
                PLAYER_BLACK,
            )
        )

    def test_black_king_can_capture_forward(self):
        self.clear_board()

        board = self.game.board

        board.set_cell(
            4,
            3,
            BLACK_KING,
        )

        board.set_cell(
            5,
            4,
            WHITE_MAN,
        )

        move = (
            4,
            3,
            6,
            5,
        )

        self.assertTrue(
            CheckersRules.is_valid_move(
                board,
                move,
                PLAYER_BLACK,
            )
        )

    def test_white_king_can_capture_backward(self):
        self.clear_board()

        board = self.game.board

        board.set_cell(
            3,
            2,
            WHITE_KING,
        )

        board.set_cell(
            4,
            3,
            BLACK_MAN,
        )

        move = (
            3,
            2,
            5,
            4,
        )

        self.assertTrue(
            CheckersRules.is_valid_move(
                board,
                move,
                PLAYER_WHITE,
            )
        )

    def test_white_king_can_capture_forward(self):
        self.clear_board()

        board = self.game.board

        board.set_cell(
            3,
            2,
            WHITE_KING,
        )

        board.set_cell(
            2,
            1,
            BLACK_MAN,
        )

        move = (
            3,
            2,
            1,
            0,
        )

        self.assertTrue(
            CheckersRules.is_valid_move(
                board,
                move,
                PLAYER_WHITE,
            )
        )

    # --------------------------------------------------
    # BLOCKED PLAYER TESTS
    # --------------------------------------------------

    def test_player_with_piece_but_no_legal_move_is_loser(self):
        self.clear_board()

        board = self.game.board

        # The only black piece.
        board.set_cell(
            2,
            1,
            BLACK_MAN,
        )

        # Opponent pieces block both forward diagonals.
        board.set_cell(
            3,
            0,
            WHITE_MAN,
        )

        board.set_cell(
            3,
            2,
            WHITE_MAN,
        )

        # Occupy both capture landing squares.
        # Therefore black cannot jump either white piece.
        board.set_cell(
            4,
            1,
            WHITE_MAN,
        )

        board.set_cell(
            4,
            3,
            WHITE_MAN,
        )

        moves = CheckersRules.get_legal_moves(
            board,
            PLAYER_BLACK,
        )

        self.assertEqual(
            moves,
            [],
        )

    def test_blocked_black_has_no_legal_move(self):
        self.clear_board()

        board = self.game.board

        # The only black piece.
        board.set_cell(
            2,
            1,
            BLACK_MAN,
        )

        # Block normal movement.
        board.set_cell(
            3,
            0,
            WHITE_MAN,
        )

        board.set_cell(
            3,
            2,
            WHITE_MAN,
        )

        # Block possible captures.
        board.set_cell(
            4,
            1,
            WHITE_MAN,
        )

        board.set_cell(
            4,
            3,
            WHITE_MAN,
        )

        self.assertFalse(
            CheckersRules.has_any_legal_move(
                board,
                PLAYER_BLACK,
            )
        )

    # --------------------------------------------------
    # MULTI-CAPTURE TESTS
    # --------------------------------------------------

    def test_multi_capture_requires_same_piece(self):
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

    def test_multi_capture_ends_when_no_capture_remains(self):
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

        first_move = (
            2,
            1,
            4,
            3,
        )

        self.assertTrue(
            self.game.make_move(first_move)
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

    # --------------------------------------------------
    # PROMOTION DURING CAPTURE
    # --------------------------------------------------

    def test_black_promotion_during_capture(self):
        self.clear_board()

        self.game.current_player = PLAYER_BLACK

        self.game.board.set_cell(
            5,
            2,
            BLACK_MAN,
        )

        self.game.board.set_cell(
            6,
            3,
            WHITE_MAN,
        )

        move = (
            5,
            2,
            7,
            4,
        )

        self.assertTrue(
            self.game.make_move(move)
        )

        self.assertEqual(
            self.game.board.get_cell(
                7,
                4,
            ),
            BLACK_KING,
        )

        self.assertFalse(
            self.game.is_in_multi_capture()
        )

        self.assertEqual(
            self.game.current_player,
            PLAYER_WHITE,
        )

    def test_white_promotion_during_capture(self):
        self.clear_board()

        self.game.current_player = PLAYER_WHITE

        self.game.board.set_cell(
            2,
            5,
            WHITE_MAN,
        )

        self.game.board.set_cell(
            1,
            4,
            BLACK_MAN,
        )

        move = (
            2,
            5,
            0,
            3,
        )

        self.assertTrue(
            self.game.make_move(move)
        )

        self.assertEqual(
            self.game.board.get_cell(
                0,
                3,
            ),
            WHITE_KING,
        )

        self.assertFalse(
            self.game.is_in_multi_capture()
        )

        self.assertEqual(
            self.game.current_player,
            PLAYER_BLACK,
        )

    # --------------------------------------------------
    # GAME FREEZE / GAME OVER
    # --------------------------------------------------

    def test_game_is_frozen_after_game_over(self):
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
            self.game.get_game_state(),
            GAME_OVER,
        )

        move_after_game_over = (
            4,
            3,
            5,
            2,
        )

        self.assertFalse(
            self.game.make_move(
                move_after_game_over
            )
        )

    def test_no_legal_move_for_current_player_ends_game(self):
        self.clear_board()

        # Black is the current player.
        self.game.current_player = PLAYER_BLACK

        # Black has a separate legal piece so that the
        # position itself is not already a Black loss.
        self.game.board.set_cell(
            5,
            0,
            BLACK_MAN,
        )

        # White's only piece.
        self.game.board.set_cell(
            2,
            1,
            WHITE_MAN,
        )

        # Block both normal forward moves for White.
        # White moves toward decreasing row numbers.
        self.game.board.set_cell(
            1,
            0,
            BLACK_MAN,
        )

        self.game.board.set_cell(
            1,
            2,
            BLACK_MAN,
        )

        # White could otherwise capture the Black piece
        # at (1, 2) and land at (0, 3).
        # Occupying the landing square prevents that capture.
        self.game.board.set_cell(
            0,
            3,
            BLACK_MAN,
        )

        # Black must have at least one legal move.
        self.assertTrue(
            CheckersRules.has_any_legal_move(
                self.game.board,
                PLAYER_BLACK,
            )
        )

        # White must have no legal move.
        self.assertFalse(
            CheckersRules.has_any_legal_move(
                self.game.board,
                PLAYER_WHITE,
            )
        )

        # _finish_turn() switches Black -> White and
        # then checks White's legal moves.
        self.game._finish_turn()

        self.assertTrue(
            self.game.is_game_over()
        )

        self.assertEqual(
            self.game.get_game_state(),
            GAME_OVER,
        )

        self.assertEqual(
            self.game.get_winner(),
            PLAYER_BLACK,
        )

    # --------------------------------------------------
    # INVALID CAPTURE TESTS
    # --------------------------------------------------

    def test_capture_cannot_jump_over_own_piece(self):
        self.clear_board()

        self.game.board.set_cell(
            2,
            1,
            BLACK_MAN,
        )

        self.game.board.set_cell(
            3,
            2,
            BLACK_MAN,
        )

        move = (
            2,
            1,
            4,
            3,
        )

        self.assertFalse(
            CheckersRules.is_valid_move(
                self.game.board,
                move,
                PLAYER_BLACK,
            )
        )

    def test_capture_cannot_land_on_occupied_square(self):
        self.clear_board()

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
            4,
            3,
            WHITE_MAN,
        )

        move = (
            2,
            1,
            4,
            3,
        )

        self.assertFalse(
            CheckersRules.is_valid_move(
                self.game.board,
                move,
                PLAYER_BLACK,
            )
        )

    def test_capture_requires_opponent_piece_between(self):
        self.clear_board()

        self.game.board.set_cell(
            2,
            1,
            BLACK_MAN,
        )

        move = (
            2,
            1,
            4,
            3,
        )

        self.assertFalse(
            CheckersRules.is_valid_move(
                self.game.board,
                move,
                PLAYER_BLACK,
            )
        )


if __name__ == "__main__":
    unittest.main()