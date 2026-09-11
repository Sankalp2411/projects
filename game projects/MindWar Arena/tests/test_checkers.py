# tests/test_checkers.py

import unittest

from games.checkers.board import CheckersBoard
from games.checkers.constants import (
    BLACK_KING,
    BLACK_MAN,
    BOARD_COLUMNS,
    BOARD_ROWS,
    EMPTY,
    PLAYER_BLACK,
    PLAYER_WHITE,
    WHITE_KING,
    WHITE_MAN,
)
from games.checkers.rules import CheckersRules


def create_empty_board():
    board = CheckersBoard()

    for row in range(BOARD_ROWS):
        for column in range(BOARD_COLUMNS):
            board.set_cell(
                row,
                column,
                EMPTY,
            )

    return board


class TestCheckersBoard(unittest.TestCase):

    def setUp(self):
        self.board = CheckersBoard()

    def test_board_dimensions(self):
        state = self.board.get_board_state()

        self.assertEqual(len(state), BOARD_ROWS)

        self.assertTrue(
            all(
                len(row) == BOARD_COLUMNS
                for row in state
            )
        )

    def test_initial_black_piece_count(self):
        self.assertEqual(
            self.board.count_pieces(PLAYER_BLACK),
            12,
        )

    def test_initial_white_piece_count(self):
        self.assertEqual(
            self.board.count_pieces(PLAYER_WHITE),
            12,
        )

    def test_initial_total_piece_count(self):
        total = (
            self.board.count_pieces(PLAYER_BLACK)
            + self.board.count_pieces(PLAYER_WHITE)
        )

        self.assertEqual(total, 24)

    def test_initial_black_piece_positions(self):
        positions = self.board.get_piece_positions(
            PLAYER_BLACK
        )

        self.assertEqual(len(positions), 12)

        for row, column in positions:
            self.assertEqual(
                self.board.get_cell(row, column),
                BLACK_MAN,
            )

            self.assertLessEqual(row, 2)

    def test_initial_white_piece_positions(self):
        positions = self.board.get_piece_positions(
            PLAYER_WHITE
        )

        self.assertEqual(len(positions), 12)

        for row, column in positions:
            self.assertEqual(
                self.board.get_cell(row, column),
                WHITE_MAN,
            )

            self.assertGreaterEqual(
                row,
                BOARD_ROWS - 3,
            )

    def test_initial_pieces_only_on_dark_squares(self):
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):

                piece = self.board.get_cell(
                    row,
                    column,
                )

                if piece != EMPTY:
                    self.assertTrue(
                        self.board.is_playable_square(
                            row,
                            column,
                        )
                    )

    def test_light_squares_are_empty_initially(self):
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):

                if not self.board.is_playable_square(
                    row,
                    column,
                ):
                    self.assertEqual(
                        self.board.get_cell(
                            row,
                            column,
                        ),
                        EMPTY,
                    )

    def test_invalid_position(self):
        self.assertFalse(
            self.board.is_valid_position(-1, 0)
        )

        self.assertFalse(
            self.board.is_valid_position(0, -1)
        )

        self.assertFalse(
            self.board.is_valid_position(
                BOARD_ROWS,
                0,
            )
        )

        self.assertFalse(
            self.board.is_valid_position(
                0,
                BOARD_COLUMNS,
            )
        )

    def test_invalid_get_cell(self):
        with self.assertRaises(ValueError):
            self.board.get_cell(-1, 0)

        with self.assertRaises(ValueError):
            self.board.get_cell(
                BOARD_ROWS,
                0,
            )

    def test_invalid_set_cell(self):
        with self.assertRaises(ValueError):
            self.board.set_cell(
                0,
                0,
                999,
            )

    def test_board_copy_is_independent(self):
        copied_board = self.board.copy()

        original_value = copied_board.get_cell(
            2,
            1,
        )

        copied_board.set_cell(
            2,
            1,
            EMPTY,
        )

        self.assertNotEqual(
            copied_board.get_cell(2, 1),
            original_value,
        )

        self.assertNotEqual(
            self.board.get_cell(2, 1),
            EMPTY,
        )


class TestCheckersRules(unittest.TestCase):

    def setUp(self):
        self.board = CheckersBoard()

    def test_get_opponent(self):
        self.assertEqual(
            CheckersRules.get_opponent(
                PLAYER_BLACK
            ),
            PLAYER_WHITE,
        )

        self.assertEqual(
            CheckersRules.get_opponent(
                PLAYER_WHITE
            ),
            PLAYER_BLACK,
        )

    def test_piece_identification(self):
        self.assertTrue(
            CheckersRules.is_player_piece(
                BLACK_MAN,
                PLAYER_BLACK,
            )
        )

        self.assertTrue(
            CheckersRules.is_player_piece(
                BLACK_KING,
                PLAYER_BLACK,
            )
        )

        self.assertTrue(
            CheckersRules.is_player_piece(
                WHITE_MAN,
                PLAYER_WHITE,
            )
        )

        self.assertTrue(
            CheckersRules.is_player_piece(
                WHITE_KING,
                PLAYER_WHITE,
            )
        )

        self.assertFalse(
            CheckersRules.is_player_piece(
                WHITE_MAN,
                PLAYER_BLACK,
            )
        )

    def test_man_and_king_identification(self):
        self.assertTrue(
            CheckersRules.is_man(BLACK_MAN)
        )

        self.assertTrue(
            CheckersRules.is_man(WHITE_MAN)
        )

        self.assertTrue(
            CheckersRules.is_king(BLACK_KING)
        )

        self.assertTrue(
            CheckersRules.is_king(WHITE_KING)
        )

        self.assertFalse(
            CheckersRules.is_king(BLACK_MAN)
        )

        self.assertFalse(
            CheckersRules.is_man(BLACK_KING)
        )

    def test_initial_black_moves_forward_only(self):
        moves = CheckersRules.get_legal_moves(
            self.board,
            PLAYER_BLACK,
        )

        self.assertTrue(moves)

        for move in moves:

            from_row = move[0]
            to_row = move[2]

            self.assertEqual(
                to_row - from_row,
                1,
            )

    def test_initial_white_moves_forward_only(self):
        moves = CheckersRules.get_legal_moves(
            self.board,
            PLAYER_WHITE,
        )

        self.assertTrue(moves)

        for move in moves:

            from_row = move[0]
            to_row = move[2]

            self.assertEqual(
                to_row - from_row,
                -1,
            )

    def test_initial_black_has_seven_legal_moves(self):
        moves = CheckersRules.get_legal_moves(
            self.board,
            PLAYER_BLACK,
        )

        self.assertEqual(
            len(moves),
            7,
        )

    def test_initial_white_has_seven_legal_moves(self):
        moves = CheckersRules.get_legal_moves(
            self.board,
            PLAYER_WHITE,
        )

        self.assertEqual(
            len(moves),
            7,
        )

    def test_black_simple_move(self):
        board = create_empty_board()

        board.set_cell(
            2,
            1,
            BLACK_MAN,
        )

        move = (
            2,
            1,
            3,
            0,
        )

        self.assertTrue(
            CheckersRules.is_valid_move(
                board,
                move,
                PLAYER_BLACK,
            )
        )

    def test_black_cannot_move_backward(self):
        board = create_empty_board()

        board.set_cell(
            4,
            1,
            BLACK_MAN,
        )

        move = (
            4,
            1,
            3,
            0,
        )

        self.assertFalse(
            CheckersRules.is_valid_move(
                board,
                move,
                PLAYER_BLACK,
            )
        )

    def test_white_cannot_move_backward(self):
        board = create_empty_board()

        board.set_cell(
            3,
            0,
            WHITE_MAN,
        )

        move = (
            3,
            0,
            4,
            1,
        )

        self.assertFalse(
            CheckersRules.is_valid_move(
                board,
                move,
                PLAYER_WHITE,
            )
        )

    def test_king_moves_forward(self):
        board = create_empty_board()

        board.set_cell(
            4,
            1,
            BLACK_KING,
        )

        move = (
            4,
            1,
            5,
            0,
        )

        self.assertTrue(
            CheckersRules.is_valid_move(
                board,
                move,
                PLAYER_BLACK,
            )
        )

    def test_king_moves_backward(self):
        board = create_empty_board()

        board.set_cell(
            4,
            1,
            BLACK_KING,
        )

        move = (
            4,
            1,
            3,
            0,
        )

        self.assertTrue(
            CheckersRules.is_valid_move(
                board,
                move,
                PLAYER_BLACK,
            )
        )

    def test_simple_move_cannot_land_on_occupied_square(self):
        board = create_empty_board()

        board.set_cell(
            2,
            1,
            BLACK_MAN,
        )

        board.set_cell(
            3,
            2,
            WHITE_MAN,
        )

        move = (
            2,
            1,
            3,
            2,
        )

        self.assertFalse(
            CheckersRules.is_valid_move(
                board,
                move,
                PLAYER_BLACK,
            )
        )

    def test_simple_move_cannot_land_on_light_square(self):
        board = create_empty_board()

        board.set_cell(
            3,
            0,
            BLACK_MAN,
        )

        move = (
            3,
            0,
            4,
            0,
        )

        self.assertFalse(
            CheckersRules.is_valid_move(
                board,
                move,
                PLAYER_BLACK,
            )
        )

    def test_capture_is_detected(self):
        board = create_empty_board()

        board.set_cell(
            2,
            1,
            BLACK_MAN,
        )

        board.set_cell(
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

        captures = CheckersRules.get_capture_moves(
            board,
            2,
            1,
        )

        self.assertIn(
            move,
            captures,
        )

    def test_capture_removes_opponent_piece(self):
        board = create_empty_board()

        board.set_cell(
            2,
            1,
            BLACK_MAN,
        )

        board.set_cell(
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
            CheckersRules.apply_move(
                board,
                move,
                PLAYER_BLACK,
            )
        )

        self.assertEqual(
            board.get_cell(3, 2),
            EMPTY,
        )

        self.assertEqual(
            board.get_cell(4, 3),
            BLACK_MAN,
        )

    def test_capture_is_mandatory(self):
        board = create_empty_board()

        board.set_cell(
            2,
            1,
            BLACK_MAN,
        )

        board.set_cell(
            3,
            2,
            WHITE_MAN,
        )

        legal_moves = CheckersRules.get_legal_moves(
            board,
            PLAYER_BLACK,
        )

        self.assertTrue(legal_moves)

        for move in legal_moves:
            self.assertTrue(
                CheckersRules.is_capture_move(
                    move
                )
            )

    def test_simple_moves_not_returned_when_capture_exists(self):
        board = create_empty_board()

        board.set_cell(
            2,
            1,
            BLACK_MAN,
        )

        board.set_cell(
            3,
            2,
            WHITE_MAN,
        )

        legal_moves = CheckersRules.get_legal_moves(
            board,
            PLAYER_BLACK,
        )

        simple_moves = [
            move
            for move in legal_moves
            if not CheckersRules.is_capture_move(
                move
            )
        ]

        self.assertEqual(
            simple_moves,
            [],
        )

    def test_captured_position(self):
        move = (
            2,
            1,
            4,
            3,
        )

        self.assertEqual(
            CheckersRules.get_captured_position(
                move
            ),
            (3, 2),
        )

    def test_non_capture_has_no_captured_position(self):
        move = (
            2,
            1,
            3,
            0,
        )

        self.assertIsNone(
            CheckersRules.get_captured_position(
                move
            )
        )

    def test_black_promotion(self):
        board = create_empty_board()

        board.set_cell(
            6,
            1,
            BLACK_MAN,
        )

        move = (
            6,
            1,
            7,
            0,
        )

        self.assertTrue(
            CheckersRules.apply_move(
                board,
                move,
                PLAYER_BLACK,
            )
        )

        self.assertEqual(
            board.get_cell(7, 0),
            BLACK_KING,
        )

    def test_white_promotion(self):
        board = create_empty_board()

        board.set_cell(
            1,
            2,
            WHITE_MAN,
        )

        move = (
            1,
            2,
            0,
            1,
        )

        self.assertTrue(
            CheckersRules.apply_move(
                board,
                move,
                PLAYER_WHITE,
            )
        )

        self.assertEqual(
            board.get_cell(0, 1),
            WHITE_KING,
        )

    def test_promote_piece(self):
        self.assertEqual(
            CheckersRules.promote_piece(
                BLACK_MAN
            ),
            BLACK_KING,
        )

        self.assertEqual(
            CheckersRules.promote_piece(
                WHITE_MAN
            ),
            WHITE_KING,
        )

        self.assertEqual(
            CheckersRules.promote_piece(
                BLACK_KING
            ),
            BLACK_KING,
        )

    def test_should_promote_black(self):
        self.assertTrue(
            CheckersRules.should_promote(
                BLACK_MAN,
                BOARD_ROWS - 1,
            )
        )

        self.assertFalse(
            CheckersRules.should_promote(
                BLACK_MAN,
                BOARD_ROWS - 2,
            )
        )

    def test_should_promote_white(self):
        self.assertTrue(
            CheckersRules.should_promote(
                WHITE_MAN,
                0,
            )
        )

        self.assertFalse(
            CheckersRules.should_promote(
                WHITE_MAN,
                1,
            )
        )

    def test_capture_move_detection(self):
        self.assertTrue(
            CheckersRules.is_capture_move(
                (2, 1, 4, 3)
            )
        )

        self.assertFalse(
            CheckersRules.is_capture_move(
                (2, 1, 3, 0)
            )
        )

    def test_capture_move_has_two_square_distance(self):
        move = (
            2,
            1,
            4,
            3,
        )

        self.assertEqual(
            abs(move[2] - move[0]),
            2,
        )

        self.assertEqual(
            abs(move[3] - move[1]),
            2,
        )

    def test_invalid_move_format(self):
        self.assertFalse(
            CheckersRules.is_valid_move(
                self.board,
                (1, 2, 3),
                PLAYER_BLACK,
            )
        )

        self.assertFalse(
            CheckersRules.is_valid_move(
                self.board,
                [1, 2, 3, 4],
                PLAYER_BLACK,
            )
        )

    def test_invalid_player(self):
        self.assertFalse(
            CheckersRules.is_valid_move(
                self.board,
                (2, 1, 3, 0),
                99,
            )
        )

    def test_opponent_piece_cannot_move(self):
        move = (
            5,
            0,
            4,
            1,
        )

        self.assertFalse(
            CheckersRules.is_valid_move(
                self.board,
                move,
                PLAYER_BLACK,
            )
        )

    def test_initial_position_is_not_game_over(self):
        self.assertFalse(
            CheckersRules.is_game_over(
                self.board
            )
        )

    def test_initial_position_has_no_winner(self):
        self.assertIsNone(
            CheckersRules.get_winner(
                self.board
            )
        )

    def test_zero_black_pieces_means_white_wins(self):
        board = create_empty_board()

        board.set_cell(
            5,
            0,
            WHITE_MAN,
        )

        self.assertEqual(
            CheckersRules.get_winner(board),
            PLAYER_WHITE,
        )

        self.assertTrue(
            CheckersRules.is_game_over(board)
        )

    def test_zero_white_pieces_means_black_wins(self):
        board = create_empty_board()

        board.set_cell(
            2,
            1,
            BLACK_MAN,
        )

        self.assertEqual(
            CheckersRules.get_winner(board),
            PLAYER_BLACK,
        )

        self.assertTrue(
            CheckersRules.is_game_over(board)
        )

    def test_game_evaluation_non_terminal(self):
        result = CheckersRules.evaluate_game(
            self.board
        )

        self.assertFalse(
            result.game_over
        )

        self.assertIsNone(
            result.winner
        )

        self.assertFalse(
            result.draw
        )

    def test_game_evaluation_white_wins(self):
        board = create_empty_board()

        board.set_cell(
            5,
            0,
            WHITE_MAN,
        )

        result = CheckersRules.evaluate_game(
            board
        )

        self.assertTrue(
            result.game_over
        )

        self.assertEqual(
            result.winner,
            PLAYER_WHITE,
        )

        self.assertFalse(
            result.draw
        )

    def test_game_evaluation_black_wins(self):
        board = create_empty_board()

        board.set_cell(
            2,
            1,
            BLACK_MAN,
        )

        result = CheckersRules.evaluate_game(
            board
        )

        self.assertTrue(
            result.game_over
        )

        self.assertEqual(
            result.winner,
            PLAYER_BLACK,
        )

        self.assertFalse(
            result.draw
        )

    def test_checkers_draw_is_false(self):
        self.assertFalse(
            CheckersRules.is_draw(
                self.board
            )
        )


if __name__ == "__main__":
    unittest.main()