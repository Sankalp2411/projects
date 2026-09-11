import random
import unittest

from engine.interfaces.game_result import GameResult

from games.othello.ai import OthelloAI
from games.othello.board import OthelloBoard
from games.othello.constants import (
    EMPTY,
    FIRST_PLAYER,
    GAME_MODE_AI_VS_AI,
    GAME_MODE_HUMAN_VS_AI,
    GAME_MODE_HUMAN_VS_HUMAN,
    GAME_RUNNING,
    PLAYER_BLACK,
    PLAYER_WHITE,
)
from games.othello.game import OthelloGame
from games.othello.rules import OthelloRules


class TestOthelloBoard(unittest.TestCase):

    def setUp(self):
        self.board = OthelloBoard()

    def test_board_initialization(self):
        self.assertEqual(self.board.get_empty_count(), 60)
        self.assertEqual(
            self.board.count_stones(PLAYER_BLACK),
            2,
        )
        self.assertEqual(
            self.board.count_stones(PLAYER_WHITE),
            2,
        )

    def test_initial_position(self):
        self.assertEqual(
            self.board.get_cell(3, 3),
            PLAYER_WHITE,
        )
        self.assertEqual(
            self.board.get_cell(3, 4),
            PLAYER_BLACK,
        )
        self.assertEqual(
            self.board.get_cell(4, 3),
            PLAYER_BLACK,
        )
        self.assertEqual(
            self.board.get_cell(4, 4),
            PLAYER_WHITE,
        )

    def test_all_other_cells_empty(self):
        occupied = {
            (3, 3),
            (3, 4),
            (4, 3),
            (4, 4),
        }

        for row in range(8):
            for column in range(8):
                if (row, column) not in occupied:
                    self.assertEqual(
                        self.board.get_cell(row, column),
                        EMPTY,
                    )

    def test_get_cell(self):
        self.assertEqual(
            self.board.get_cell(3, 3),
            PLAYER_WHITE,
        )

    def test_set_cell_black(self):
        self.board.set_cell(0, 0, PLAYER_BLACK)

        self.assertEqual(
            self.board.get_cell(0, 0),
            PLAYER_BLACK,
        )

    def test_set_cell_white(self):
        self.board.set_cell(0, 0, PLAYER_WHITE)

        self.assertEqual(
            self.board.get_cell(0, 0),
            PLAYER_WHITE,
        )

    def test_set_cell_empty(self):
        self.board.set_cell(3, 3, EMPTY)

        self.assertEqual(
            self.board.get_cell(3, 3),
            EMPTY,
        )

    def test_invalid_get_position(self):
        with self.assertRaises(ValueError):
            self.board.get_cell(-1, 0)

        with self.assertRaises(ValueError):
            self.board.get_cell(8, 0)

        with self.assertRaises(ValueError):
            self.board.get_cell(0, -1)

        with self.assertRaises(ValueError):
            self.board.get_cell(0, 8)

    def test_invalid_set_position(self):
        with self.assertRaises(ValueError):
            self.board.set_cell(-1, 0, PLAYER_BLACK)

        with self.assertRaises(ValueError):
            self.board.set_cell(8, 0, PLAYER_BLACK)

    def test_invalid_cell_value(self):
        with self.assertRaises(ValueError):
            self.board.set_cell(0, 0, 99)

    def test_is_valid_position(self):
        self.assertTrue(
            self.board.is_valid_position(0, 0)
        )
        self.assertTrue(
            self.board.is_valid_position(7, 7)
        )
        self.assertFalse(
            self.board.is_valid_position(-1, 0)
        )
        self.assertFalse(
            self.board.is_valid_position(8, 0)
        )

    def test_is_cell_empty(self):
        self.assertTrue(
            self.board.is_cell_empty(0, 0)
        )
        self.assertFalse(
            self.board.is_cell_empty(3, 3)
        )

    def test_available_moves_initial(self):
        moves = self.board.get_available_moves()

        self.assertEqual(len(moves), 60)

    def test_empty_count(self):
        self.assertEqual(
            self.board.get_empty_count(),
            60,
        )

        self.board.set_cell(0, 0, PLAYER_BLACK)

        self.assertEqual(
            self.board.get_empty_count(),
            59,
        )

    def test_board_full(self):
        for row in range(8):
            for column in range(8):
                self.board.set_cell(
                    row,
                    column,
                    PLAYER_BLACK,
                )

        self.assertTrue(
            self.board.is_board_full()
        )

        self.assertEqual(
            self.board.get_empty_count(),
            0,
        )

    def test_board_not_full(self):
        self.assertFalse(
            self.board.is_board_full()
        )

    def test_count_stones(self):
        self.assertEqual(
            self.board.count_stones(PLAYER_BLACK),
            2,
        )
        self.assertEqual(
            self.board.count_stones(PLAYER_WHITE),
            2,
        )

    def test_invalid_count_player(self):
        with self.assertRaises(ValueError):
            self.board.count_stones(99)

    def test_copy(self):
        copied = self.board.copy()

        self.assertIsNot(
            copied,
            self.board,
        )

        self.assertEqual(
            copied.get_board_state(),
            self.board.get_board_state(),
        )

    def test_copy_is_independent(self):
        copied = self.board.copy()

        copied.set_cell(0, 0, PLAYER_BLACK)

        self.assertEqual(
            self.board.get_cell(0, 0),
            EMPTY,
        )

    def test_board_state_is_independent(self):
        state = self.board.get_board_state()

        state[0][0] = PLAYER_BLACK

        self.assertEqual(
            self.board.get_cell(0, 0),
            EMPTY,
        )

    def test_reset(self):
        self.board.set_cell(0, 0, PLAYER_BLACK)

        self.board.reset()

        self.assertEqual(
            self.board.get_cell(0, 0),
            EMPTY,
        )
        self.assertEqual(
            self.board.count_stones(PLAYER_BLACK),
            2,
        )
        self.assertEqual(
            self.board.count_stones(PLAYER_WHITE),
            2,
        )


class TestOthelloMoveValidation(unittest.TestCase):

    def setUp(self):
        self.board = OthelloBoard()

    def test_initial_black_legal_moves(self):
        moves = OthelloRules.get_legal_moves(
            self.board,
            PLAYER_BLACK,
        )

        expected = [
            (2, 3),
            (3, 2),
            (4, 5),
            (5, 4),
        ]

        self.assertCountEqual(
            moves,
            expected,
        )

    def test_initial_white_legal_moves(self):
        moves = OthelloRules.get_legal_moves(
            self.board,
            PLAYER_WHITE,
        )

        expected = [
            (2, 4),
            (3, 5),
            (4, 2),
            (5, 3),
        ]

        self.assertCountEqual(
            moves,
            expected,
        )

    def test_occupied_cell_is_invalid(self):
        self.assertFalse(
            OthelloRules.is_valid_move(
                self.board,
                3,
                3,
                PLAYER_BLACK,
            )
        )

    def test_empty_non_flipping_cell_is_invalid(self):
        self.assertFalse(
            OthelloRules.is_valid_move(
                self.board,
                0,
                0,
                PLAYER_BLACK,
            )
        )

    def test_out_of_bounds_move_is_invalid(self):
        self.assertFalse(
            OthelloRules.is_valid_move(
                self.board,
                -1,
                0,
                PLAYER_BLACK,
            )
        )

        self.assertFalse(
            OthelloRules.is_valid_move(
                self.board,
                8,
                0,
                PLAYER_BLACK,
            )
        )

    def test_invalid_player_move(self):
        self.assertFalse(
            OthelloRules.is_valid_move(
                self.board,
                0,
                0,
                99,
            )
        )

    def test_black_initial_move(self):
        self.assertTrue(
            OthelloRules.is_valid_move(
                self.board,
                2,
                3,
                PLAYER_BLACK,
            )
        )

    def test_white_initial_move(self):
        self.assertTrue(
            OthelloRules.is_valid_move(
                self.board,
                2,
                4,
                PLAYER_WHITE,
            )
        )


class TestOthelloFlipping(unittest.TestCase):

    def create_empty_board(self):
        board = OthelloBoard()

        for row in range(8):
            for column in range(8):
                board.set_cell(
                    row,
                    column,
                    EMPTY,
                )

        return board

    def test_single_direction_horizontal_flip(self):
        board = self.create_empty_board()

        board.set_cell(0, 0, PLAYER_BLACK)
        board.set_cell(0, 1, PLAYER_WHITE)
        board.set_cell(0, 2, PLAYER_WHITE)

        flips = OthelloRules.get_flips(
            board,
            0,
            3,
            PLAYER_BLACK,
        )

        self.assertCountEqual(
            flips,
            [
                (0, 1),
                (0, 2),
            ],
        )

    def test_single_direction_vertical_flip(self):
        board = self.create_empty_board()

        board.set_cell(0, 0, PLAYER_BLACK)
        board.set_cell(1, 0, PLAYER_WHITE)
        board.set_cell(2, 0, PLAYER_WHITE)

        flips = OthelloRules.get_flips(
            board,
            3,
            0,
            PLAYER_BLACK,
        )

        self.assertCountEqual(
            flips,
            [
                (1, 0),
                (2, 0),
            ],
        )

    def test_diagonal_flip(self):
        board = self.create_empty_board()

        board.set_cell(0, 0, PLAYER_BLACK)
        board.set_cell(1, 1, PLAYER_WHITE)
        board.set_cell(2, 2, PLAYER_WHITE)

        flips = OthelloRules.get_flips(
            board,
            3,
            3,
            PLAYER_BLACK,
        )

        self.assertCountEqual(
            flips,
            [
                (1, 1),
                (2, 2),
            ],
        )

    def test_no_bracket_no_flip(self):
        board = self.create_empty_board()

        board.set_cell(0, 0, PLAYER_WHITE)
        board.set_cell(0, 1, PLAYER_WHITE)

        flips = OthelloRules.get_flips(
            board,
            0,
            2,
            PLAYER_BLACK,
        )

        self.assertEqual(flips, [])

    def test_empty_cell_blocks_flip(self):
        board = self.create_empty_board()

        board.set_cell(0, 0, PLAYER_BLACK)
        board.set_cell(0, 1, PLAYER_WHITE)
        board.set_cell(0, 4, PLAYER_BLACK)

        flips = OthelloRules.get_flips(
            board,
            0,
            3,
            PLAYER_BLACK,
        )

        self.assertEqual(flips, [])

    def test_multi_direction_flip(self):
        board = self.create_empty_board()

        center_row = 3
        center_column = 3

        directions = OthelloRules._DIRECTIONS

        for direction_row, direction_column in directions:
            white_row = (
                center_row + direction_row
            )
            white_column = (
                center_column + direction_column
            )

            black_row = (
                center_row + direction_row * 2
            )
            black_column = (
                center_column + direction_column * 2
            )

            if (
                0 <= white_row < 8
                and 0 <= white_column < 8
                and 0 <= black_row < 8
                and 0 <= black_column < 8
            ):
                board.set_cell(
                    white_row,
                    white_column,
                    PLAYER_WHITE,
                )

                board.set_cell(
                    black_row,
                    black_column,
                    PLAYER_BLACK,
                )

        flips = OthelloRules.get_flips(
            board,
            center_row,
            center_column,
            PLAYER_BLACK,
        )

        expected_flips = []

        for direction_row, direction_column in directions:
            white_row = (
                center_row + direction_row
            )
            white_column = (
                center_column + direction_column
            )

            black_row = (
                center_row + direction_row * 2
            )
            black_column = (
                center_column + direction_column * 2
            )

            if (
                0 <= white_row < 8
                and 0 <= white_column < 8
                and 0 <= black_row < 8
                and 0 <= black_column < 8
            ):
                expected_flips.append(
                    (
                        white_row,
                        white_column,
                    )
                )

        self.assertCountEqual(
            flips,
            expected_flips,
        )

    def test_apply_move_places_disc(self):
        board = OthelloBoard()

        success = OthelloRules.apply_move(
            board,
            2,
            3,
            PLAYER_BLACK,
        )

        self.assertTrue(success)

        self.assertEqual(
            board.get_cell(2, 3),
            PLAYER_BLACK,
        )

    def test_apply_move_flips_disc(self):
        board = OthelloBoard()

        OthelloRules.apply_move(
            board,
            2,
            3,
            PLAYER_BLACK,
        )

        self.assertEqual(
            board.get_cell(3, 3),
            PLAYER_BLACK,
        )

    def test_apply_invalid_move(self):
        board = OthelloBoard()

        success = OthelloRules.apply_move(
            board,
            0,
            0,
            PLAYER_BLACK,
        )

        self.assertFalse(success)

    def test_no_flip_through_empty_cell(self):
        board = self.create_empty_board()

        board.set_cell(0, 1, PLAYER_WHITE)
        board.set_cell(0, 3, PLAYER_BLACK)

        self.assertFalse(
            OthelloRules.is_valid_move(
                board,
                0,
                0,
                PLAYER_BLACK,
            )
        )

        flips = OthelloRules.get_flips(
            board,
            0,
            0,
            PLAYER_BLACK,
        )

        self.assertEqual(flips, [])

    def test_opponent(self):
        self.assertEqual(
            OthelloRules.get_opponent(PLAYER_BLACK),
            PLAYER_WHITE,
        )

        self.assertEqual(
            OthelloRules.get_opponent(PLAYER_WHITE),
            PLAYER_BLACK,
        )

    def test_invalid_opponent(self):
        with self.assertRaises(ValueError):
            OthelloRules.get_opponent(99)


class TestOthelloPassAndTermination(unittest.TestCase):

    def test_initial_board_not_game_over(self):
        board = OthelloBoard()

        self.assertFalse(
            OthelloRules.is_game_over(board)
        )

    def test_full_board_game_over(self):
        board = OthelloBoard()

        for row in range(8):
            for column in range(8):
                board.set_cell(
                    row,
                    column,
                    PLAYER_BLACK,
                )

        self.assertTrue(
            OthelloRules.is_game_over(board)
        )

    def test_two_players_no_moves_game_over(self):
        board = OthelloBoard()

        for row in range(8):
            for column in range(8):
                board.set_cell(
                    row,
                    column,
                    PLAYER_BLACK,
                )

        board.set_cell(
            7,
            7,
            EMPTY,
        )

        self.assertFalse(
            OthelloRules.can_player_move(
                board,
                PLAYER_BLACK,
            )
        )

        self.assertFalse(
            OthelloRules.can_player_move(
                board,
                PLAYER_WHITE,
            )
        )

        self.assertTrue(
            OthelloRules.is_game_over(board)
        )

    def test_one_player_no_move_does_not_end_game(self):
        board = OthelloBoard()

        for row in range(8):
            for column in range(8):
                board.set_cell(
                    row,
                    column,
                    EMPTY,
                )

        board.set_cell(
            0,
            0,
            PLAYER_BLACK,
        )

        board.set_cell(
            0,
            1,
            PLAYER_WHITE,
        )

        self.assertTrue(
            OthelloRules.can_player_move(
                board,
                PLAYER_BLACK,
            )
        )

        self.assertFalse(
            OthelloRules.can_player_move(
                board,
                PLAYER_WHITE,
            )
        )

        self.assertFalse(
            OthelloRules.is_game_over(board)
        )

    def test_two_consecutive_passes_end_game(self):
        board = OthelloBoard()

        for row in range(8):
            for column in range(8):
                board.set_cell(
                    row,
                    column,
                    PLAYER_BLACK,
                )

        board.set_cell(
            7,
            7,
            EMPTY,
        )

        game = OthelloGame(
            renderer=None,
            game_mode=GAME_MODE_HUMAN_VS_HUMAN,
        )

        game.board = board
        game.current_player = PLAYER_WHITE
        game.result.reset()
        game.game_state = GAME_RUNNING
        game.consecutive_passes = 0

        first_pass = game.pass_turn()

        self.assertTrue(first_pass)

        self.assertEqual(
            game.current_player,
            PLAYER_BLACK,
        )

        self.assertEqual(
            game.consecutive_passes,
            1,
        )

        second_pass = game.pass_turn()

        self.assertTrue(second_pass)

        self.assertTrue(
            game.is_game_over()
        )

    def test_can_player_move_initial(self):
        board = OthelloBoard()

        self.assertTrue(
            OthelloRules.can_player_move(
                board,
                PLAYER_BLACK,
            )
        )

        self.assertTrue(
            OthelloRules.can_player_move(
                board,
                PLAYER_WHITE,
            )
        )


class TestOthelloWinnerAndDraw(unittest.TestCase):

    def test_black_wins(self):
        board = OthelloBoard()

        for row in range(8):
            for column in range(8):
                board.set_cell(
                    row,
                    column,
                    PLAYER_BLACK,
                )

        self.assertEqual(
            OthelloRules.get_winner(board),
            PLAYER_BLACK,
        )

    def test_white_wins(self):
        board = OthelloBoard()

        for row in range(8):
            for column in range(8):
                board.set_cell(
                    row,
                    column,
                    PLAYER_WHITE,
                )

        self.assertEqual(
            OthelloRules.get_winner(board),
            PLAYER_WHITE,
        )

    def test_equal_count_is_draw(self):
        board = OthelloBoard()

        for row in range(8):
            for column in range(8):
                if (row + column) % 2 == 0:
                    board.set_cell(
                        row,
                        column,
                        PLAYER_BLACK,
                    )
                else:
                    board.set_cell(
                        row,
                        column,
                        PLAYER_WHITE,
                    )

        self.assertEqual(
            board.count_stones(PLAYER_BLACK),
            32,
        )

        self.assertEqual(
            board.count_stones(PLAYER_WHITE),
            32,
        )

        self.assertTrue(
            OthelloRules.is_game_over(board)
        )

        self.assertTrue(
            OthelloRules.is_draw(board)
        )

    def test_not_draw_during_game(self):
        board = OthelloBoard()

        self.assertFalse(
            OthelloRules.is_draw(board)
        )

    def test_evaluate_game_not_over(self):
        board = OthelloBoard()

        result = OthelloRules.evaluate_game(board)

        self.assertFalse(result.game_over)
        self.assertIsNone(result.winner)
        self.assertFalse(result.draw)

    def test_evaluate_black_win(self):
        board = OthelloBoard()

        for row in range(8):
            for column in range(8):
                board.set_cell(
                    row,
                    column,
                    PLAYER_BLACK,
                )

        result = OthelloRules.evaluate_game(board)

        self.assertTrue(result.game_over)
        self.assertEqual(
            result.winner,
            PLAYER_BLACK,
        )
        self.assertFalse(result.draw)

    def test_evaluate_white_win(self):
        board = OthelloBoard()

        for row in range(8):
            for column in range(8):
                board.set_cell(
                    row,
                    column,
                    PLAYER_WHITE,
                )

        result = OthelloRules.evaluate_game(board)

        self.assertTrue(result.game_over)
        self.assertEqual(
            result.winner,
            PLAYER_WHITE,
        )
        self.assertFalse(result.draw)

    def test_evaluate_draw(self):
        board = OthelloBoard()

        for row in range(8):
            for column in range(8):
                if (row + column) % 2 == 0:
                    board.set_cell(
                        row,
                        column,
                        PLAYER_BLACK,
                    )
                else:
                    board.set_cell(
                        row,
                        column,
                        PLAYER_WHITE,
                    )

        result = OthelloRules.evaluate_game(board)

        self.assertTrue(result.game_over)
        self.assertTrue(result.draw)
        self.assertIsNone(result.winner)


class TestOthelloAI(unittest.TestCase):

    def setUp(self):
        self.ai = OthelloAI()

    def test_initial_state_not_initialized(self):
        self.assertFalse(
            self.ai.initialized
        )

    def test_initialize(self):
        self.ai.initialize()

        self.assertTrue(
            self.ai.initialized
        )

    def test_select_action_before_initialize(self):
        board = OthelloBoard()

        state = {
            "board": board.get_board_state(),
            "current_player": PLAYER_BLACK,
        }

        action = self.ai.select_action(state)

        self.assertIsNone(action)

    def test_select_action_after_initialize(self):
        self.ai.initialize()

        board = OthelloBoard()

        state = {
            "board": board.get_board_state(),
            "current_player": PLAYER_BLACK,
        }

        action = self.ai.select_action(state)

        self.assertIsNotNone(action)

        self.assertIn(
            action,
            OthelloRules.get_legal_moves(
                board,
                PLAYER_BLACK,
            ),
        )

    def test_ai_action_is_legal(self):
        self.ai.initialize()

        board = OthelloBoard()

        state = {
            "board": board.get_board_state(),
            "current_player": PLAYER_BLACK,
        }

        for _ in range(20):
            action = self.ai.select_action(state)

            if action is not None:
                self.assertIn(
                    action,
                    OthelloRules.get_legal_moves(
                        board,
                        PLAYER_BLACK,
                    ),
                )

    def test_ai_returns_none_when_no_moves(self):
        self.ai.initialize()

        board = OthelloBoard()

        for row in range(8):
            for column in range(8):
                board.set_cell(
                    row,
                    column,
                    PLAYER_BLACK,
                )

        state = {
            "board": board.get_board_state(),
            "current_player": PLAYER_WHITE,
        }

        action = self.ai.select_action(state)

        self.assertIsNone(action)

    def test_ai_invalid_player(self):
        self.ai.initialize()

        board = OthelloBoard()

        state = {
            "board": board.get_board_state(),
            "current_player": 99,
        }

        self.assertIsNone(
            self.ai.select_action(state)
        )

    def test_ai_empty_state(self):
        self.ai.initialize()

        self.assertIsNone(
            self.ai.select_action(None)
        )

    def test_ai_reset(self):
        self.ai.initialize()

        self.assertTrue(
            self.ai.initialized
        )

        self.ai.reset()

        self.assertFalse(
            self.ai.initialized
        )

    def test_ai_get_action(self):
        self.ai.initialize()

        game = OthelloGame(
            renderer=None,
            game_mode=GAME_MODE_HUMAN_VS_AI,
        )

        game.initialize()

        action = self.ai.get_action(game)

        self.assertIn(
            action,
            game.get_legal_moves(),
        )


class TestOthelloGameController(unittest.TestCase):

    def create_game(
        self,
        mode=GAME_MODE_HUMAN_VS_HUMAN,
    ):
        game = OthelloGame(
            renderer=None,
            game_mode=mode,
        )

        game.initialize()

        return game

    def test_game_creation(self):
        game = self.create_game()

        self.assertIsNotNone(game.board)
        self.assertIsNotNone(game.result)

    def test_game_initial_state(self):
        game = self.create_game()

        self.assertEqual(
            game.game_state,
            GAME_RUNNING,
        )

        self.assertEqual(
            game.current_player,
            FIRST_PLAYER,
        )

    def test_initial_counts(self):
        game = self.create_game()

        self.assertEqual(
            game.get_black_count(),
            2,
        )

        self.assertEqual(
            game.get_white_count(),
            2,
        )

    def test_initial_legal_moves(self):
        game = self.create_game()

        self.assertEqual(
            len(game.get_legal_moves()),
            4,
        )

    def test_make_valid_move(self):
        game = self.create_game()

        success = game.make_move(2, 3)

        self.assertTrue(success)

        self.assertEqual(
            game.board.get_cell(2, 3),
            PLAYER_BLACK,
        )

    def test_make_invalid_move(self):
        game = self.create_game()

        success = game.make_move(0, 0)

        self.assertFalse(success)
        self.assertEqual(
            game.move_count,
            0,
        )

    def test_turn_switches_after_move(self):
        game = self.create_game()

        self.assertEqual(
            game.current_player,
            PLAYER_BLACK,
        )

        game.make_move(2, 3)

        self.assertEqual(
            game.current_player,
            PLAYER_WHITE,
        )

    def test_move_count(self):
        game = self.create_game()

        self.assertEqual(
            game.move_count,
            0,
        )

        game.make_move(2, 3)

        self.assertEqual(
            game.move_count,
            1,
        )

    def test_total_stones_after_moves(self):
        game = self.create_game()

        initial_stones = (
            game.get_black_count()
            + game.get_white_count()
        )

        self.assertEqual(
            initial_stones,
            4,
        )

        for _ in range(5):
            legal_moves = game.get_legal_moves()

            if not legal_moves:
                break

            move = legal_moves[0]

            game.make_move(
                move[0],
                move[1],
            )

            if game.is_game_over():
                break

        total_stones = (
            game.get_black_count()
            + game.get_white_count()
        )

        self.assertEqual(
            total_stones,
            4 + game.move_count,
        )

    def test_get_state(self):
        game = self.create_game()

        state = game.get_state()

        expected_keys = {
            "board",
            "current_player",
            "winner",
            "game_state",
            "game_over",
            "draw",
            "move_count",
            "consecutive_passes",
            "black_count",
            "white_count",
            "legal_moves",
        }

        self.assertTrue(
            expected_keys.issubset(state.keys())
        )

    def test_get_board(self):
        game = self.create_game()

        self.assertIs(
            game.get_board(),
            game.board,
        )

    def test_get_current_player(self):
        game = self.create_game()

        self.assertEqual(
            game.get_current_player(),
            PLAYER_BLACK,
        )

    def test_get_winner_initially_none(self):
        game = self.create_game()

        self.assertIsNone(
            game.get_winner()
        )

    def test_get_result(self):
        game = self.create_game()

        self.assertIs(
            game.get_result(),
            game.result,
        )

    def test_get_game_state(self):
        game = self.create_game()

        self.assertEqual(
            game.get_game_state(),
            GAME_RUNNING,
        )

    def test_is_game_over_initially_false(self):
        game = self.create_game()

        self.assertFalse(
            game.is_game_over()
        )

    def test_is_frozen_initially_false(self):
        game = self.create_game()

        self.assertFalse(
            game.is_frozen()
        )

    def test_game_reset(self):
        game = self.create_game()

        game.make_move(2, 3)

        self.assertEqual(
            game.move_count,
            1,
        )

        game.reset()

        self.assertEqual(
            game.move_count,
            0,
        )

        self.assertEqual(
            game.get_black_count(),
            2,
        )

        self.assertEqual(
            game.get_white_count(),
            2,
        )

        self.assertFalse(
            game.is_game_over()
        )

    def test_starting_player_alternates(self):
        game = self.create_game()

        first_player = game.current_player

        game.reset()

        second_player = game.current_player

        self.assertNotEqual(
            first_player,
            second_player,
        )

    def test_human_vs_human_controller(self):
        game = self.create_game(
            GAME_MODE_HUMAN_VS_HUMAN
        )

        controller = game.get_current_controller()

        self.assertIs(
            controller,
            game.human_player,
        )

    def test_human_vs_ai_controller_black(self):
        game = self.create_game(
            GAME_MODE_HUMAN_VS_AI
        )

        game.current_player = PLAYER_BLACK

        controller = game.get_current_controller()

        self.assertIs(
            controller,
            game.human_player,
        )

    def test_human_vs_ai_controller_white(self):
        game = self.create_game(
            GAME_MODE_HUMAN_VS_AI
        )

        game.current_player = PLAYER_WHITE

        controller = game.get_current_controller()

        self.assertIs(
            controller,
            game.ai,
        )

    def test_ai_vs_ai_controller(self):
        game = self.create_game(
            GAME_MODE_AI_VS_AI
        )

        controller = game.get_current_controller()

        self.assertIs(
            controller,
            game.ai,
        )

    def test_invalid_move_coordinates(self):
        game = self.create_game()

        self.assertFalse(
            game.make_move(-1, 0)
        )

        self.assertFalse(
            game.make_move(8, 0)
        )

        self.assertFalse(
            game.make_move(0, -1)
        )

        self.assertFalse(
            game.make_move(0, 8)
        )

    def test_shutdown(self):
        game = self.create_game()

        game.shutdown()

    def test_game_can_play_multiple_legal_moves(self):
        game = self.create_game()

        moves_played = 0

        for _ in range(10):
            legal_moves = game.get_legal_moves()

            if not legal_moves:
                break

            row, column = legal_moves[0]

            success = game.make_move(
                row,
                column,
            )

            if success:
                moves_played += 1

            if game.is_game_over():
                break

        self.assertGreater(
            moves_played,
            0,
        )


class TestGameResult(unittest.TestCase):

    def test_initial_result(self):
        result = GameResult()

        self.assertIsNone(result.winner)
        self.assertFalse(result.game_over)
        self.assertFalse(result.draw)

        self.assertEqual(
            result.winning_cells,
            [],
        )

    def test_reset(self):
        result = GameResult()

        result.winner = PLAYER_BLACK
        result.game_over = True
        result.draw = True
        result.winning_cells = [(0, 0)]

        result.reset()

        self.assertIsNone(result.winner)
        self.assertFalse(result.game_over)
        self.assertFalse(result.draw)

        self.assertEqual(
            result.winning_cells,
            [],
        )

    def test_has_winner(self):
        result = GameResult()

        self.assertFalse(
            result.has_winner()
        )

        result.winner = PLAYER_BLACK

        self.assertTrue(
            result.has_winner()
        )

    def test_is_draw(self):
        result = GameResult()

        self.assertFalse(
            result.is_draw()
        )

        result.draw = True

        self.assertTrue(
            result.is_draw()
        )

    def test_is_game_over(self):
        result = GameResult()

        self.assertFalse(
            result.is_game_over()
        )

        result.game_over = True

        self.assertTrue(
            result.is_game_over()
        )


class TestOthelloIntegration(unittest.TestCase):

    def test_basic_game_sequence(self):
        game = OthelloGame(
            renderer=None,
            game_mode=GAME_MODE_HUMAN_VS_HUMAN,
        )

        game.initialize()

        self.assertEqual(
            game.move_count,
            0,
        )

        legal_moves = game.get_legal_moves()

        self.assertEqual(
            len(legal_moves),
            4,
        )

        row, column = legal_moves[0]

        self.assertTrue(
            game.make_move(
                row,
                column,
            )
        )

        self.assertEqual(
            game.move_count,
            1,
        )

        self.assertEqual(
            game.current_player,
            PLAYER_WHITE,
        )

    def test_repeated_legal_moves(self):
        game = OthelloGame(
            renderer=None,
            game_mode=GAME_MODE_HUMAN_VS_HUMAN,
        )

        game.initialize()

        successful_moves = 0

        for _ in range(20):
            legal_moves = game.get_legal_moves()

            if not legal_moves:
                break

            move = legal_moves[
                random.randrange(
                    len(legal_moves)
                )
            ]

            if game.make_move(
                move[0],
                move[1],
            ):
                successful_moves += 1

            if game.is_game_over():
                break

        self.assertGreater(
            successful_moves,
            0,
        )

        self.assertEqual(
            game.move_count,
            successful_moves,
        )


if __name__ == "__main__":
    unittest.main()