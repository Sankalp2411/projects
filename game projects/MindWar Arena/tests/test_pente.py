"""
Pente Test Suite
================

Phase 5 — Pente
Step 14 — Testing

This file contains the complete Pente test suite.

Test Categories:
    1. Basic Board Tests
    2. Five-in-a-Row Tests
    3. Capture Tests
    4. Victory Tests
    5. Draw Tests
    6. Game Controller Tests
    7. AI Tests
    8. Integration / Regression Tests
"""

from games.pente.ai import PenteAI
from games.pente.board import PenteBoard
from games.pente.constants import (
    BOARD_ROWS,
    BOARD_COLUMNS,
    EMPTY,
    PLAYER_BLACK,
    PLAYER_WHITE,
    FIRST_PLAYER,
    GAME_RUNNING,
    GAME_DRAW,
    GAME_OVER,
    GAME_MODE_HUMAN_VS_HUMAN,
    GAME_MODE_HUMAN_VS_AI,
    CAPTURE_WIN_PAIRS,
    NO_WINNER,
)
from games.pente.game import PenteGame
from games.pente.rules import PenteRules


# ======================================================================
# TEST HELPERS
# ======================================================================

def create_empty_board():
    """Create and return a fresh empty Pente board."""
    return PenteBoard()


def place_stones(board, player, cells):
    """Place multiple stones for a player."""
    for row, column in cells:
        assert board.place_stone(row, column, player)


def assert_empty_cells(board, cells):
    """Verify that all specified cells are empty."""
    for row, column in cells:
        assert board.get_cell(row, column) == EMPTY


# ======================================================================
# 1. BASIC BOARD TESTS
# ======================================================================

def test_board_initial_state():
    board = create_empty_board()

    assert BOARD_ROWS == 19
    assert BOARD_COLUMNS == 19

    assert board.get_empty_count() == 19 * 19
    assert board.count_stones(PLAYER_BLACK) == 0
    assert board.count_stones(PLAYER_WHITE) == 0
    assert not board.is_board_full()


def test_board_valid_positions():
    board = create_empty_board()

    assert board.is_valid_position(0, 0)
    assert board.is_valid_position(18, 18)
    assert board.is_valid_position(9, 9)

    assert not board.is_valid_position(-1, 0)
    assert not board.is_valid_position(0, -1)
    assert not board.is_valid_position(19, 0)
    assert not board.is_valid_position(0, 19)


def test_board_stone_placement():
    board = create_empty_board()

    assert board.place_stone(
        9,
        9,
        PLAYER_BLACK,
    )

    assert board.get_cell(9, 9) == PLAYER_BLACK
    assert board.count_stones(PLAYER_BLACK) == 1
    assert board.get_empty_count() == 19 * 19 - 1


def test_board_rejects_invalid_placement():
    board = create_empty_board()

    assert not board.place_stone(
        -1,
        0,
        PLAYER_BLACK,
    )

    assert not board.place_stone(
        19,
        19,
        PLAYER_BLACK,
    )

    assert not board.place_stone(
        0,
        0,
        999,
    )


def test_board_rejects_occupied_cell():
    board = create_empty_board()

    assert board.place_stone(
        5,
        5,
        PLAYER_BLACK,
    )

    assert not board.place_stone(
        5,
        5,
        PLAYER_WHITE,
    )

    assert board.get_cell(5, 5) == PLAYER_BLACK


def test_board_remove_stone():
    board = create_empty_board()

    assert board.place_stone(
        5,
        5,
        PLAYER_BLACK,
    )

    assert board.remove_stone(5, 5)

    assert board.get_cell(5, 5) == EMPTY
    assert board.count_stones(PLAYER_BLACK) == 0


def test_board_copy_is_independent():
    board = create_empty_board()

    board.place_stone(
        5,
        5,
        PLAYER_BLACK,
    )

    copied_board = board.copy()

    assert copied_board.get_cell(5, 5) == PLAYER_BLACK

    copied_board.remove_stone(5, 5)

    assert board.get_cell(5, 5) == PLAYER_BLACK
    assert copied_board.get_cell(5, 5) == EMPTY


def test_board_reset():
    board = create_empty_board()

    board.place_stone(
        5,
        5,
        PLAYER_BLACK,
    )

    board.place_stone(
        6,
        6,
        PLAYER_WHITE,
    )

    board.reset()

    assert board.get_empty_count() == 19 * 19
    assert board.count_stones(PLAYER_BLACK) == 0
    assert board.count_stones(PLAYER_WHITE) == 0


# ======================================================================
# 2. FIVE-IN-A-ROW TESTS
# ======================================================================

def test_horizontal_five_in_a_row():
    board = create_empty_board()

    place_stones(
        board,
        PLAYER_BLACK,
        [
            (5, 5),
            (5, 6),
            (5, 7),
            (5, 8),
            (5, 9),
        ],
    )

    assert PenteRules.check_winner(board) == PLAYER_BLACK


def test_vertical_five_in_a_row():
    board = create_empty_board()

    place_stones(
        board,
        PLAYER_WHITE,
        [
            (5, 5),
            (6, 5),
            (7, 5),
            (8, 5),
            (9, 5),
        ],
    )

    assert PenteRules.check_winner(board) == PLAYER_WHITE


def test_diagonal_down_right_five():
    board = create_empty_board()

    place_stones(
        board,
        PLAYER_BLACK,
        [
            (5, 5),
            (6, 6),
            (7, 7),
            (8, 8),
            (9, 9),
        ],
    )

    assert PenteRules.check_winner(board) == PLAYER_BLACK


def test_diagonal_down_left_five():
    board = create_empty_board()

    place_stones(
        board,
        PLAYER_WHITE,
        [
            (5, 9),
            (6, 8),
            (7, 7),
            (8, 6),
            (9, 5),
        ],
    )

    assert PenteRules.check_winner(board) == PLAYER_WHITE


def test_four_in_a_row_is_not_win():
    board = create_empty_board()

    place_stones(
        board,
        PLAYER_BLACK,
        [
            (5, 5),
            (5, 6),
            (5, 7),
            (5, 8),
        ],
    )

    assert PenteRules.check_winner(board) == 0


def test_broken_line_is_not_win():
    board = create_empty_board()

    place_stones(
        board,
        PLAYER_BLACK,
        [
            (5, 5),
            (5, 6),
            (5, 8),
            (5, 9),
            (5, 10),
        ],
    )

    assert PenteRules.check_winner(board) == 0


def test_winning_cells_are_returned():
    board = create_empty_board()

    winning_cells = [
        (5, 5),
        (5, 6),
        (5, 7),
        (5, 8),
        (5, 9),
    ]

    place_stones(
        board,
        PLAYER_BLACK,
        winning_cells,
    )

    result = PenteRules.get_winning_cells(board)

    assert result == winning_cells


# ======================================================================
# 3. CAPTURE TESTS
# ======================================================================

def test_horizontal_capture():
    board = create_empty_board()

    board.place_stone(5, 5, PLAYER_BLACK)
    board.place_stone(5, 6, PLAYER_WHITE)
    board.place_stone(5, 7, PLAYER_WHITE)
    board.place_stone(5, 8, PLAYER_BLACK)

    captures = PenteRules.get_captures(
        board,
        5,
        8,
        PLAYER_BLACK,
    )

    assert len(captures) == 1

    assert set(captures[0]) == {
        (5, 6),
        (5, 7),
    }


def test_vertical_capture():
    board = create_empty_board()

    board.place_stone(5, 5, PLAYER_BLACK)
    board.place_stone(6, 5, PLAYER_WHITE)
    board.place_stone(7, 5, PLAYER_WHITE)
    board.place_stone(8, 5, PLAYER_BLACK)

    captures = PenteRules.get_captures(
        board,
        8,
        5,
        PLAYER_BLACK,
    )

    assert len(captures) == 1

    assert set(captures[0]) == {
        (6, 5),
        (7, 5),
    }


def test_diagonal_capture():
    board = create_empty_board()

    board.place_stone(5, 5, PLAYER_BLACK)
    board.place_stone(6, 6, PLAYER_WHITE)
    board.place_stone(7, 7, PLAYER_WHITE)
    board.place_stone(8, 8, PLAYER_BLACK)

    captures = PenteRules.get_captures(
        board,
        8,
        8,
        PLAYER_BLACK,
    )

    assert len(captures) == 1

    assert set(captures[0]) == {
        (6, 6),
        (7, 7),
    }


def test_reverse_direction_capture():
    board = create_empty_board()

    board.place_stone(5, 8, PLAYER_BLACK)
    board.place_stone(5, 7, PLAYER_WHITE)
    board.place_stone(5, 6, PLAYER_WHITE)
    board.place_stone(5, 5, PLAYER_BLACK)

    captures = PenteRules.get_captures(
        board,
        5,
        5,
        PLAYER_BLACK,
    )

    assert len(captures) == 1

    assert set(captures[0]) == {
        (5, 6),
        (5, 7),
    }


def test_invalid_capture_pattern():
    board = create_empty_board()

    board.place_stone(5, 5, PLAYER_BLACK)
    board.place_stone(5, 6, PLAYER_WHITE)
    board.place_stone(5, 7, PLAYER_WHITE)

    captures = PenteRules.get_captures(
        board,
        5,
        5,
        PLAYER_BLACK,
    )

    assert captures == []


def test_capture_cells_are_removed():
    board = create_empty_board()

    board.place_stone(5, 5, PLAYER_BLACK)
    board.place_stone(5, 6, PLAYER_WHITE)
    board.place_stone(5, 7, PLAYER_WHITE)
    board.place_stone(5, 8, PLAYER_BLACK)

    captures = PenteRules.get_captures(
        board,
        5,
        8,
        PLAYER_BLACK,
    )

    captured_count = PenteRules.apply_captures(
        board,
        captures,
    )

    assert captured_count == 2

    assert_empty_cells(
        board,
        [
            (5, 6),
            (5, 7),
        ],
    )


def test_find_captures_returns_cells():
    board = create_empty_board()

    board.place_stone(5, 5, PLAYER_BLACK)
    board.place_stone(5, 6, PLAYER_WHITE)
    board.place_stone(5, 7, PLAYER_WHITE)
    board.place_stone(5, 8, PLAYER_BLACK)

    captured_cells = PenteRules.find_captures(
        board,
        5,
        8,
        PLAYER_BLACK,
    )

    assert set(captured_cells) == {
        (5, 6),
        (5, 7),
    }


# ======================================================================
# 4. VICTORY TESTS
# ======================================================================

def test_five_in_a_row_victory():
    board = create_empty_board()

    place_stones(
        board,
        PLAYER_BLACK,
        [
            (5, 5),
            (5, 6),
            (5, 7),
            (5, 8),
            (5, 9),
        ],
    )

    result = PenteRules.evaluate_game(
        board,
        {
            PLAYER_BLACK: 0,
            PLAYER_WHITE: 0,
        },
    )

    assert result.game_over
    assert not result.draw
    assert result.winner == PLAYER_BLACK


def test_capture_victory():
    board = create_empty_board()

    result = PenteRules.evaluate_game(
        board,
        {
            PLAYER_BLACK: CAPTURE_WIN_PAIRS,
            PLAYER_WHITE: 0,
        },
    )

    assert result.game_over
    assert not result.draw
    assert result.winner == PLAYER_BLACK


def test_white_capture_victory():
    board = create_empty_board()

    result = PenteRules.evaluate_game(
        board,
        {
            PLAYER_BLACK: 0,
            PLAYER_WHITE: CAPTURE_WIN_PAIRS,
        },
    )

    assert result.game_over
    assert not result.draw
    assert result.winner == PLAYER_WHITE


def test_game_continues_without_winner():
    board = create_empty_board()

    board.place_stone(
        5,
        5,
        PLAYER_BLACK,
    )

    result = PenteRules.evaluate_game(
        board,
        {
            PLAYER_BLACK: 0,
            PLAYER_WHITE: 0,
        },
    )

    assert not result.game_over
    assert not result.draw
    assert result.winner is None


# ======================================================================
# 5. DRAW TESTS
# ======================================================================

def test_empty_board_is_not_draw():
    board = create_empty_board()

    assert not PenteRules.is_draw(
        board,
        {
            PLAYER_BLACK: 0,
            PLAYER_WHITE: 0,
        },
    )


def test_full_board_without_winner_is_draw():
    board = create_empty_board()

    # Deterministic full-board pattern that avoids
    # five consecutive stones in every supported direction.
    #
    # Pattern:
    #     (row + 2 * column) % 5 == 0 -> BLACK
    #     otherwise                    -> WHITE
    #
    # This is specifically chosen so that no horizontal,
    # vertical, or diagonal sequence contains five identical
    # stones.

    for row in range(BOARD_ROWS):
        for column in range(BOARD_COLUMNS):
            player = (
                PLAYER_BLACK
                if (row + 2 * column) % 5 == 0
                else PLAYER_WHITE
            )

            board.set_cell(
                row,
                column,
                player,
            )

    assert board.is_board_full()

    assert PenteRules.check_winner(board) == NO_WINNER

    assert PenteRules.is_draw(
        board,
        {
            PLAYER_BLACK: 0,
            PLAYER_WHITE: 0,
        },
    )


# ======================================================================
# 6. GAME CONTROLLER TESTS
# ======================================================================

def test_game_initial_state():
    game = PenteGame(
        renderer=None,
        game_mode=GAME_MODE_HUMAN_VS_HUMAN,
    )

    assert game.board is not None
    assert game.current_player == FIRST_PLAYER
    assert game.move_count == 0

    assert game.capture_counts[PLAYER_BLACK] == 0
    assert game.capture_counts[PLAYER_WHITE] == 0


def test_game_reset():
    game = PenteGame(
        renderer=None,
        game_mode=GAME_MODE_HUMAN_VS_HUMAN,
    )

    game.board.place_stone(
        5,
        5,
        PLAYER_BLACK,
    )

    game.move_count = 1
    game.capture_counts[PLAYER_BLACK] = 2

    game.reset()

    assert game.move_count == 0
    assert game.capture_counts[PLAYER_BLACK] == 0
    assert game.capture_counts[PLAYER_WHITE] == 0
    assert game.board.get_empty_count() == 19 * 19
    assert game.game_state == GAME_RUNNING


def test_game_switch_player():
    game = PenteGame(
        renderer=None,
        game_mode=GAME_MODE_HUMAN_VS_HUMAN,
    )

    assert game.current_player == PLAYER_BLACK

    game.switch_player()

    assert game.current_player == PLAYER_WHITE

    game.switch_player()

    assert game.current_player == PLAYER_BLACK


def test_game_make_move():
    game = PenteGame(
        renderer=None,
        game_mode=GAME_MODE_HUMAN_VS_HUMAN,
    )

    game.reset()

    starting_player = game.current_player

    assert game.make_move(
        5,
        5,
    )

    assert game.board.get_cell(
        5,
        5,
    ) == starting_player

    assert game.move_count == 1

    assert game.current_player != starting_player


def test_game_rejects_occupied_move():
    game = PenteGame(
        renderer=None,
        game_mode=GAME_MODE_HUMAN_VS_HUMAN,
    )

    game.reset()

    assert game.make_move(5, 5)

    current_player = game.current_player

    assert not game.make_move(5, 5)

    assert game.current_player == current_player


def test_game_rejects_invalid_move():
    game = PenteGame(
        renderer=None,
        game_mode=GAME_MODE_HUMAN_VS_HUMAN,
    )

    game.reset()

    assert not game.make_move(-1, 0)
    assert not game.make_move(19, 19)


def test_game_state_contains_required_data():
    game = PenteGame(
        renderer=None,
        game_mode=GAME_MODE_HUMAN_VS_HUMAN,
    )

    game.reset()

    state = game.get_state()

    assert "board" in state
    assert "current_player" in state
    assert "winner" in state
    assert "game_state" in state
    assert "game_over" in state
    assert "draw" in state
    assert "move_count" in state
    assert "capture_counts" in state


# ======================================================================
# 7. AI TESTS
# ======================================================================

def test_ai_initialization():
    ai = PenteAI()

    assert not ai.initialized

    ai.initialize()

    assert ai.initialized


def test_ai_returns_legal_move():
    ai = PenteAI()
    ai.initialize()

    board = create_empty_board()

    state = {
        "board": board.get_board_state(),
    }

    move = ai.select_action(state)

    assert move is not None

    row, column = move

    assert board.is_valid_position(
        row,
        column,
    )

    assert board.is_cell_empty(
        row,
        column,
    )


def test_ai_does_not_select_occupied_cell():
    ai = PenteAI()
    ai.initialize()

    board = create_empty_board()

    board.place_stone(
        5,
        5,
        PLAYER_BLACK,
    )

    state = {
        "board": board.get_board_state(),
    }

    for _ in range(20):
        move = ai.select_action(state)

        assert move is not None

        row, column = move

        assert board.get_cell(
            row,
            column,
        ) == EMPTY


def test_ai_returns_none_on_full_board():
    ai = PenteAI()
    ai.initialize()

    board = create_empty_board()

    for row in range(BOARD_ROWS):
        for column in range(BOARD_COLUMNS):
            player = (
                PLAYER_BLACK
                if (row + column) % 2 == 0
                else PLAYER_WHITE
            )

            board.set_cell(
                row,
                column,
                player,
            )

    state = {
        "board": board.get_board_state(),
    }

    assert ai.select_action(state) is None


def test_ai_reset():
    ai = PenteAI()

    ai.initialize()

    assert ai.initialized

    ai.reset()

    assert not ai.initialized


def test_ai_get_action():
    ai = PenteAI()
    ai.initialize()

    game = PenteGame(
        renderer=None,
        game_mode=GAME_MODE_HUMAN_VS_AI,
    )

    game.reset()

    move = ai.get_action(game)

    assert move is not None

    row, column = move

    assert game.board.is_valid_position(
        row,
        column,
    )

    assert game.board.is_cell_empty(
        row,
        column,
    )


# ======================================================================
# 8. INTEGRATION / REGRESSION TESTS
# ======================================================================

def test_pente_game_human_vs_human_creation():
    game = PenteGame(
        renderer=None,
        game_mode=GAME_MODE_HUMAN_VS_HUMAN,
    )

    assert game.game_mode == GAME_MODE_HUMAN_VS_HUMAN
    assert game.player_black is game.human_player
    assert game.player_white is game.human_player


def test_pente_game_human_vs_ai_creation():
    game = PenteGame(
        renderer=None,
        game_mode=GAME_MODE_HUMAN_VS_AI,
    )

    assert game.game_mode == GAME_MODE_HUMAN_VS_AI
    assert game.player_black is game.human_player
    assert game.player_white is game.ai_player


def test_pente_capture_through_game_controller():
    game = PenteGame(
        renderer=None,
        game_mode=GAME_MODE_HUMAN_VS_HUMAN,
    )

    game.reset()

    # Force a capture pattern before the final move.
    game.board.place_stone(
        5,
        5,
        PLAYER_BLACK,
    )

    game.board.place_stone(
        5,
        6,
        PLAYER_WHITE,
    )

    game.board.place_stone(
        5,
        7,
        PLAYER_WHITE,
    )

    game.current_player = PLAYER_BLACK

    assert game.make_move(
        5,
        8,
    )

    assert game.capture_counts[
        PLAYER_BLACK
    ] == 1

    assert game.board.get_cell(
        5,
        6,
    ) == EMPTY

    assert game.board.get_cell(
        5,
        7,
    ) == EMPTY


def test_pente_game_detects_five_in_a_row():
    game = PenteGame(
        renderer=None,
        game_mode=GAME_MODE_HUMAN_VS_HUMAN,
    )

    game.reset()

    winning_cells = [
        (5, 5),
        (5, 6),
        (5, 7),
        (5, 8),
    ]

    for cell in winning_cells:
        game.board.place_stone(
            cell[0],
            cell[1],
            PLAYER_BLACK,
        )

    game.current_player = PLAYER_BLACK

    assert game.make_move(
        5,
        9,
    )

    assert game.is_game_over()
    assert game.get_winner() == PLAYER_BLACK
    assert game.game_state == GAME_OVER


def test_pente_game_state_after_move():
    game = PenteGame(
        renderer=None,
        game_mode=GAME_MODE_HUMAN_VS_HUMAN,
    )

    game.reset()

    assert game.make_move(
        9,
        9,
    )

    state = game.get_state()

    assert state["move_count"] == 1
    assert state["game_over"] is False
    assert state["draw"] is False
    assert state["board"][9][9] != EMPTY


def test_pente_multiple_moves():
    game = PenteGame(
        renderer=None,
        game_mode=GAME_MODE_HUMAN_VS_HUMAN,
    )

    game.reset()

    moves = [
        (9, 9),
        (8, 8),
        (9, 10),
        (8, 9),
        (10, 9),
        (7, 7),
    ]

    for move in moves:
        assert game.make_move(
            move[0],
            move[1],
        )

    assert game.move_count == len(moves)


# ======================================================================
# TEST RUNNER
# ======================================================================

def run_tests():
    """
    Execute all Pente tests manually.

    This allows the file to be executed directly with:

        python tests/test_pente.py
    """

    tests = [
        # --------------------------------------------------------------
        # 1. Board
        # --------------------------------------------------------------
        test_board_initial_state,
        test_board_valid_positions,
        test_board_stone_placement,
        test_board_rejects_invalid_placement,
        test_board_rejects_occupied_cell,
        test_board_remove_stone,
        test_board_copy_is_independent,
        test_board_reset,

        # --------------------------------------------------------------
        # 2. Five-in-a-row
        # --------------------------------------------------------------
        test_horizontal_five_in_a_row,
        test_vertical_five_in_a_row,
        test_diagonal_down_right_five,
        test_diagonal_down_left_five,
        test_four_in_a_row_is_not_win,
        test_broken_line_is_not_win,
        test_winning_cells_are_returned,

        # --------------------------------------------------------------
        # 3. Captures
        # --------------------------------------------------------------
        test_horizontal_capture,
        test_vertical_capture,
        test_diagonal_capture,
        test_reverse_direction_capture,
        test_invalid_capture_pattern,
        test_capture_cells_are_removed,
        test_find_captures_returns_cells,

        # --------------------------------------------------------------
        # 4. Victory
        # --------------------------------------------------------------
        test_five_in_a_row_victory,
        test_capture_victory,
        test_white_capture_victory,
        test_game_continues_without_winner,

        # --------------------------------------------------------------
        # 5. Draw
        # --------------------------------------------------------------
        test_empty_board_is_not_draw,
        test_full_board_without_winner_is_draw,

        # --------------------------------------------------------------
        # 6. Game Controller
        # --------------------------------------------------------------
        test_game_initial_state,
        test_game_reset,
        test_game_switch_player,
        test_game_make_move,
        test_game_rejects_occupied_move,
        test_game_rejects_invalid_move,
        test_game_state_contains_required_data,

        # --------------------------------------------------------------
        # 7. AI
        # --------------------------------------------------------------
        test_ai_initialization,
        test_ai_returns_legal_move,
        test_ai_does_not_select_occupied_cell,
        test_ai_returns_none_on_full_board,
        test_ai_reset,
        test_ai_get_action,

        # --------------------------------------------------------------
        # 8. Integration
        # --------------------------------------------------------------
        test_pente_game_human_vs_human_creation,
        test_pente_game_human_vs_ai_creation,
        test_pente_capture_through_game_controller,
        test_pente_game_detects_five_in_a_row,
        test_pente_game_state_after_move,
        test_pente_multiple_moves,
    ]

    passed = 0
    failed = 0

    print("=" * 70)
    print("MINDWAR ARENA — PENTE TEST SUITE")
    print("=" * 70)

    for test in tests:
        try:
            test()
            print(f"[PASS] {test.__name__}")
            passed += 1

        except Exception as error:
            print(f"[FAIL] {test.__name__}")
            print(f"       {type(error).__name__}: {error}")
            failed += 1

    print()
    print("=" * 70)
    print(f"TOTAL : {len(tests)}")
    print(f"PASSED: {passed}")
    print(f"FAILED: {failed}")
    print("=" * 70)

    if failed == 0:
        print("RESULT: ALL PENTE TESTS PASSED")
    else:
        print("RESULT: PENTE TEST SUITE FAILED")

    return failed == 0


if __name__ == "__main__":
    success = run_tests()

    if not success:
        raise SystemExit(1)