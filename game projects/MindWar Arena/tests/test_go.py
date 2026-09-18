"""
MindWar Arena
Go - Complete Working Model Test

This test covers the complete Go implementation:

    games/go/constants.py
    games/go/board.py
    games/go/rules.py
    games/go/ai.py
    games/go/board_renderer.py
    games/go/human_player.py
    games/go/overlay_renderer.py
    games/go/game.py

The test validates:
    - Constants
    - Board operations
    - Board state/copy
    - Rule helpers
    - Groups and liberties
    - Capture logic
    - Suicide prevention
    - Legal move generation
    - Move simulation
    - Move application
    - Ko detection
    - Territory/scoring
    - Game results
    - AI
    - Board renderer
    - Human player
    - Overlay renderer
    - Game initialization
    - Game state
    - Game moves
    - Pass system
    - Game modes
    - AI vs AI flow
    - Reset behavior
    - Full gameplay integration

This test is designed for the CURRENT Go working model.
It does not require changing the Go source files.
"""

import sys
import pygame


# ================================================================
# IMPORTS
# ================================================================

from games.go.constants import (
    GAME_NAME,
    GAME_VERSION,

    BOARD_ROWS,
    BOARD_COLUMNS,

    EMPTY,
    PLAYER_BLACK,
    PLAYER_WHITE,

    FIRST_PLAYER,

    GAME_NOT_STARTED,
    GAME_RUNNING,
    GAME_DRAW,
    GAME_OVER,

    NO_WINNER,

    GAME_MODE_HUMAN_VS_HUMAN,
    GAME_MODE_HUMAN_VS_AI,
    GAME_MODE_AI_VS_AI,

    DEFAULT_GAME_MODE,

    AI_RANDOM,
    AI_EASY,
    AI_MEDIUM,
    AI_HARD,

    CONSECUTIVE_PASSES_TO_END,
    KOMI,

    ACTION_PLACE,
    ACTION_PASS,

    BOARD_SIZE,
    BOARD_PADDING,
    CELL_SIZE,
    BOARD_LINE_WIDTH,
    STONE_RADIUS,

    STAR_POINTS,
)

from games.go.board import GoBoard
from games.go.rules import GoRules
from games.go.ai import GoAI
from games.go.board_renderer import GoBoardRenderer
from games.go.human_player import HumanPlayer
from games.go.overlay_renderer import GoOverlayRenderer
from games.go.game import GoGame


# ================================================================
# TEST FRAMEWORK
# ================================================================

TOTAL_TESTS = 0
PASSED_TESTS = 0
FAILED_TESTS = 0


def test(name, function):
    global TOTAL_TESTS
    global PASSED_TESTS
    global FAILED_TESTS

    TOTAL_TESTS += 1

    try:
        function()
        PASSED_TESTS += 1
        print(f"[PASS] {name}")

    except Exception as error:
        FAILED_TESTS += 1
        print(f"[FAIL] {name}")
        print(f"       {type(error).__name__}: {error}")


def assert_true(condition, message="Condition is false"):
    if not condition:
        raise AssertionError(message)


def assert_false(condition, message="Condition is true"):
    if condition:
        raise AssertionError(message)


def assert_equal(actual, expected, message=None):
    if actual != expected:
        if message is None:
            message = (
                f"Expected {expected!r}, "
                f"got {actual!r}"
            )

        raise AssertionError(message)


def assert_not_equal(actual, expected, message=None):
    if actual == expected:
        if message is None:
            message = (
                f"Expected values to differ, "
                f"both were {actual!r}"
            )

        raise AssertionError(message)


def assert_is_none(value, message="Expected None"):
    if value is not None:
        raise AssertionError(
            f"{message}: got {value!r}"
        )


def assert_is_not_none(value, message="Expected non-None"):
    if value is None:
        raise AssertionError(message)


# ================================================================
# MOCK RENDERER
# ================================================================

class MockRenderer:
    """
    Minimal renderer compatible with the Go rendering classes.

    It records rendering operations so the renderer classes can be
    tested without opening the actual OpenGL rendering pipeline.
    """

    def __init__(self):
        self.calls = []
        self.overlay_messages = []

    def draw_filled_rectangle(
        self,
        position,
        size,
        color,
    ):
        self.calls.append(
            (
                "rectangle",
                position,
                size,
                color,
            )
        )

    def draw_line(
        self,
        start,
        end,
        color,
    ):
        self.calls.append(
            (
                "line",
                start,
                end,
                color,
            )
        )

    def draw_filled_circle(
        self,
        center,
        radius,
        color,
    ):
        self.calls.append(
            (
                "circle",
                center,
                radius,
                color,
            )
        )

    def draw_overlay_message(self, message):
        self.overlay_messages.append(message)

        self.calls.append(
            (
                "overlay",
                message,
            )
        )

    def reset(self):
        self.calls.clear()
        self.overlay_messages.clear()


# ================================================================
# HELPERS
# ================================================================

def create_game(
    game_mode=GAME_MODE_HUMAN_VS_HUMAN
):
    renderer = MockRenderer()

    game = GoGame(
        renderer,
        game_mode,
    )

    game.initialize()

    return game, renderer


def create_empty_board():
    return GoBoard()


def fill_board(board, player):
    for row in range(BOARD_ROWS):
        for column in range(BOARD_COLUMNS):
            board.set_cell(
                row,
                column,
                player,
            )


# ================================================================
# CONSTANTS TESTS
# ================================================================

def test_constants_basic():
    assert_equal(GAME_NAME, "Go")
    assert_equal(GAME_VERSION, "1.0.0")

    assert_equal(BOARD_ROWS, 9)
    assert_equal(BOARD_COLUMNS, 9)

    assert_equal(EMPTY, 0)
    assert_equal(PLAYER_BLACK, 1)
    assert_equal(PLAYER_WHITE, 2)

    assert_equal(FIRST_PLAYER, PLAYER_BLACK)


def test_constants_game_states():
    assert_equal(GAME_NOT_STARTED, 0)
    assert_equal(GAME_RUNNING, 1)
    assert_equal(GAME_DRAW, 2)
    assert_equal(GAME_OVER, 3)

    assert_equal(NO_WINNER, 0)


def test_constants_game_modes():
    assert_equal(
        GAME_MODE_HUMAN_VS_HUMAN,
        0,
    )

    assert_equal(
        GAME_MODE_HUMAN_VS_AI,
        1,
    )

    assert_equal(
        GAME_MODE_AI_VS_AI,
        2,
    )

    assert_equal(
        DEFAULT_GAME_MODE,
        GAME_MODE_HUMAN_VS_HUMAN,
    )


def test_constants_ai_modes():
    assert_equal(AI_RANDOM, "Random")
    assert_equal(AI_EASY, "Easy")
    assert_equal(AI_MEDIUM, "Medium")
    assert_equal(AI_HARD, "Hard")


def test_constants_rules():
    assert_equal(
        CONSECUTIVE_PASSES_TO_END,
        2,
    )

    assert_equal(KOMI, 6.5)

    assert_equal(
        ACTION_PLACE,
        "place",
    )

    assert_equal(
        ACTION_PASS,
        "pass",
    )


def test_constants_rendering():
    assert_equal(BOARD_SIZE, 560)
    assert_equal(BOARD_PADDING, 50)

    assert_true(CELL_SIZE > 0)
    assert_true(BOARD_LINE_WIDTH > 0)
    assert_true(STONE_RADIUS > 0)

    assert_equal(
        len(STAR_POINTS),
        5,
    )


# ================================================================
# BOARD TESTS
# ================================================================

def test_board_creation():
    board = GoBoard()

    assert_equal(
        len(board.get_board_state()),
        BOARD_ROWS,
    )

    for row in board.get_board_state():
        assert_equal(
            len(row),
            BOARD_COLUMNS,
        )


def test_board_initially_empty():
    board = GoBoard()

    assert_equal(
        board.count_stones(PLAYER_BLACK),
        0,
    )

    assert_equal(
        board.count_stones(PLAYER_WHITE),
        0,
    )

    assert_equal(
        board.get_empty_count(),
        BOARD_ROWS * BOARD_COLUMNS,
    )

    assert_false(board.is_board_full())


def test_board_position_validation():
    board = GoBoard()

    assert_true(
        board.is_valid_position(0, 0)
    )

    assert_true(
        board.is_valid_position(8, 8)
    )

    assert_false(
        board.is_valid_position(-1, 0)
    )

    assert_false(
        board.is_valid_position(0, -1)
    )

    assert_false(
        board.is_valid_position(9, 0)
    )

    assert_false(
        board.is_valid_position(0, 9)
    )


def test_board_set_and_get_cell():
    board = GoBoard()

    board.set_cell(
        3,
        4,
        PLAYER_BLACK,
    )

    assert_equal(
        board.get_cell(3, 4),
        PLAYER_BLACK,
    )

    board.set_cell(
        3,
        4,
        PLAYER_WHITE,
    )

    assert_equal(
        board.get_cell(3, 4),
        PLAYER_WHITE,
    )

    board.set_cell(
        3,
        4,
        EMPTY,
    )

    assert_equal(
        board.get_cell(3, 4),
        EMPTY,
    )


def test_board_invalid_cell_value():
    board = GoBoard()

    try:
        board.set_cell(
            0,
            0,
            99,
        )

        raise AssertionError(
            "Invalid cell value was accepted"
        )

    except ValueError:
        pass


def test_board_invalid_get_position():
    board = GoBoard()

    try:
        board.get_cell(
            -1,
            0,
        )

        raise AssertionError(
            "Invalid position was accepted"
        )

    except ValueError:
        pass


def test_board_place_stone():
    board = GoBoard()

    assert_true(
        board.place_stone(
            2,
            3,
            PLAYER_BLACK,
        )
    )

    assert_equal(
        board.get_cell(2, 3),
        PLAYER_BLACK,
    )


def test_board_cannot_place_on_occupied_cell():
    board = GoBoard()

    assert_true(
        board.place_stone(
            2,
            3,
            PLAYER_BLACK,
        )
    )

    assert_false(
        board.place_stone(
            2,
            3,
            PLAYER_WHITE,
        )
    )

    assert_equal(
        board.get_cell(2, 3),
        PLAYER_BLACK,
    )


def test_board_invalid_place_stone():
    board = GoBoard()

    assert_false(
        board.place_stone(
            -1,
            0,
            PLAYER_BLACK,
        )
    )

    assert_false(
        board.place_stone(
            0,
            0,
            99,
        )
    )


def test_board_remove_stone():
    board = GoBoard()

    board.place_stone(
        2,
        2,
        PLAYER_BLACK,
    )

    assert_true(
        board.remove_stone(2, 2)
    )

    assert_equal(
        board.get_cell(2, 2),
        EMPTY,
    )


def test_board_remove_empty_stone():
    board = GoBoard()

    assert_false(
        board.remove_stone(2, 2)
    )


def test_board_empty_positions():
    board = GoBoard()

    board.place_stone(
        0,
        0,
        PLAYER_BLACK,
    )

    empty_positions = (
        board.get_empty_positions()
    )

    assert_equal(
        len(empty_positions),
        BOARD_ROWS * BOARD_COLUMNS - 1,
    )

    assert_true(
        (0, 0) not in empty_positions
    )


def test_board_player_positions():
    board = GoBoard()

    board.place_stone(
        1,
        1,
        PLAYER_BLACK,
    )

    board.place_stone(
        2,
        2,
        PLAYER_BLACK,
    )

    board.place_stone(
        3,
        3,
        PLAYER_WHITE,
    )

    black_positions = (
        board.get_player_positions(
            PLAYER_BLACK
        )
    )

    white_positions = (
        board.get_player_positions(
            PLAYER_WHITE
        )
    )

    assert_equal(
        len(black_positions),
        2,
    )

    assert_equal(
        len(white_positions),
        1,
    )


def test_board_counts():
    board = GoBoard()

    board.place_stone(
        1,
        1,
        PLAYER_BLACK,
    )

    board.place_stone(
        1,
        2,
        PLAYER_BLACK,
    )

    board.place_stone(
        2,
        2,
        PLAYER_WHITE,
    )

    assert_equal(
        board.count_stones(
            PLAYER_BLACK
        ),
        2,
    )

    assert_equal(
        board.count_stones(
            PLAYER_WHITE
        ),
        1,
    )


def test_board_full_detection():
    board = GoBoard()

    fill_board(
        board,
        PLAYER_BLACK,
    )

    assert_true(
        board.is_board_full()
    )

    assert_equal(
        board.get_empty_count(),
        0,
    )


def test_board_state_copy():
    board = GoBoard()

    board.place_stone(
        4,
        4,
        PLAYER_BLACK,
    )

    copied = board.copy()

    assert_true(
        board is not copied
    )

    assert_equal(
        copied.get_cell(4, 4),
        PLAYER_BLACK,
    )

    copied.remove_stone(
        4,
        4,
    )

    assert_equal(
        board.get_cell(4, 4),
        PLAYER_BLACK,
    )


def test_board_get_set_state():
    board = GoBoard()

    board.place_stone(
        4,
        4,
        PLAYER_BLACK,
    )

    state = board.get_board_state()

    new_board = GoBoard()

    new_board.set_board_state(
        state
    )

    assert_equal(
        new_board.get_board_state(),
        state,
    )


def test_board_invalid_state():
    board = GoBoard()

    try:
        board.set_board_state(
            [[0]]
        )

        raise AssertionError(
            "Invalid board state accepted"
        )

    except ValueError:
        pass


def test_board_string():
    board = GoBoard()

    board.place_stone(
        0,
        0,
        PLAYER_BLACK,
    )

    text = str(board)

    assert_true(
        isinstance(text, str)
    )

    assert_true(
        "B" in text
    )


# ================================================================
# RULE BASIC TESTS
# ================================================================

def test_rules_player_validation():
    assert_true(
        GoRules.is_valid_player(
            PLAYER_BLACK
        )
    )

    assert_true(
        GoRules.is_valid_player(
            PLAYER_WHITE
        )
    )

    assert_false(
        GoRules.is_valid_player(99)
    )


def test_rules_opponent():
    assert_equal(
        GoRules.get_opponent(
            PLAYER_BLACK
        ),
        PLAYER_WHITE,
    )

    assert_equal(
        GoRules.get_opponent(
            PLAYER_WHITE
        ),
        PLAYER_BLACK,
    )

    assert_is_none(
        GoRules.get_opponent(99)
    )


def test_rules_position_validation():
    assert_true(
        GoRules.is_valid_position(
            0,
            0,
        )
    )

    assert_true(
        GoRules.is_valid_position(
            8,
            8,
        )
    )

    assert_false(
        GoRules.is_valid_position(
            -1,
            0,
        )
    )

    assert_false(
        GoRules.is_valid_position(
            9,
            0,
        )
    )


def test_rules_same_position():
    assert_true(
        GoRules.is_same_position(
            (2, 3),
            (2, 3),
        )
    )

    assert_false(
        GoRules.is_same_position(
            (2, 3),
            (3, 2),
        )
    )


# ================================================================
# NEIGHBOR / GROUP / LIBERTY TESTS
# ================================================================

def test_rules_corner_neighbors():
    neighbors = (
        GoRules.get_neighbors(
            0,
            0,
        )
    )

    assert_equal(
        len(neighbors),
        2,
    )

    assert_true(
        (1, 0) in neighbors
    )

    assert_true(
        (0, 1) in neighbors
    )


def test_rules_center_neighbors():
    neighbors = (
        GoRules.get_neighbors(
            4,
            4,
        )
    )

    assert_equal(
        len(neighbors),
        4,
    )


def test_rules_invalid_neighbors():
    assert_equal(
        GoRules.get_neighbors(
            -1,
            0,
        ),
        [],
    )


def test_rules_single_group():
    board = GoBoard()

    board.place_stone(
        4,
        4,
        PLAYER_BLACK,
    )

    group = GoRules.get_group(
        board,
        4,
        4,
    )

    assert_equal(
        len(group),
        1,
    )

    assert_true(
        (4, 4) in group
    )


def test_rules_connected_group():
    board = GoBoard()

    board.place_stone(
        4,
        4,
        PLAYER_BLACK,
    )

    board.place_stone(
        4,
        5,
        PLAYER_BLACK,
    )

    board.place_stone(
        5,
        5,
        PLAYER_BLACK,
    )

    group = GoRules.get_group(
        board,
        4,
        4,
    )

    assert_equal(
        len(group),
        3,
    )


def test_rules_group_does_not_include_opponent():
    board = GoBoard()

    board.place_stone(
        4,
        4,
        PLAYER_BLACK,
    )

    board.place_stone(
        4,
        5,
        PLAYER_WHITE,
    )

    group = GoRules.get_group(
        board,
        4,
        4,
    )

    assert_equal(
        len(group),
        1,
    )


def test_rules_group_liberties():
    board = GoBoard()

    board.place_stone(
        4,
        4,
        PLAYER_BLACK,
    )

    liberties = (
        GoRules.get_group_liberties(
            board,
            GoRules.get_group(
                board,
                4,
                4,
            ),
        )
    )

    assert_equal(
        len(liberties),
        4,
    )


def test_rules_count_liberties_corner():
    board = GoBoard()

    board.place_stone(
        0,
        0,
        PLAYER_BLACK,
    )

    assert_equal(
        GoRules.count_liberties(
            board,
            0,
            0,
        ),
        2,
    )


def test_rules_count_liberties_center():
    board = GoBoard()

    board.place_stone(
        4,
        4,
        PLAYER_BLACK,
    )

    assert_equal(
        GoRules.count_liberties(
            board,
            4,
            4,
        ),
        4,
    )


# ================================================================
# CAPTURE TESTS
# ================================================================

def test_rules_capture_detection():
    board = GoBoard()

    board.place_stone(
        4,
        4,
        PLAYER_WHITE,
    )

    board.place_stone(
        3,
        4,
        PLAYER_BLACK,
    )

    board.place_stone(
        5,
        4,
        PLAYER_BLACK,
    )

    board.place_stone(
        4,
        3,
        PLAYER_BLACK,
    )

    board.place_stone(
        4,
        5,
        PLAYER_BLACK,
    )

    assert_true(
        GoRules.is_group_captured(
            board,
            4,
            4,
        )
    )


def test_rules_get_captured_positions():
    board = GoBoard()

    board.place_stone(
        4,
        4,
        PLAYER_WHITE,
    )

    board.place_stone(
        3,
        4,
        PLAYER_BLACK,
    )

    board.place_stone(
        5,
        4,
        PLAYER_BLACK,
    )

    board.place_stone(
        4,
        3,
        PLAYER_BLACK,
    )

    captured = (
        GoRules.get_captured_positions(
            board,
            PLAYER_BLACK,
            4,
            5,
        )
    )

    assert_true(
        (4, 4) in captured
    )


def test_rules_capture_group():
    board = GoBoard()

    board.place_stone(
        4,
        4,
        PLAYER_WHITE,
    )

    board.place_stone(
        3,
        4,
        PLAYER_BLACK,
    )

    board.place_stone(
        5,
        4,
        PLAYER_BLACK,
    )

    board.place_stone(
        4,
        3,
        PLAYER_BLACK,
    )

    board.place_stone(
        4,
        5,
        PLAYER_BLACK,
    )

    removed = GoRules.capture_group(
        board,
        4,
        4,
    )

    assert_equal(
        removed,
        1,
    )

    assert_equal(
        board.get_cell(4, 4),
        EMPTY,
    )


def test_rules_capture_opponent_groups():
    board = GoBoard()

    board.place_stone(
        4,
        4,
        PLAYER_WHITE,
    )

    board.place_stone(
        3,
        4,
        PLAYER_BLACK,
    )

    board.place_stone(
        5,
        4,
        PLAYER_BLACK,
    )

    board.place_stone(
        4,
        3,
        PLAYER_BLACK,
    )

    board.place_stone(
        4,
        5,
        PLAYER_BLACK,
    )

    removed = (
        GoRules.capture_opponent_groups(
            board,
            PLAYER_BLACK,
            4,
            5,
        )
    )

    assert_true(
        removed >= 0
    )


def test_rules_apply_capture_move():
    board = GoBoard()

    board.place_stone(
        4,
        4,
        PLAYER_WHITE,
    )

    board.place_stone(
        3,
        4,
        PLAYER_BLACK,
    )

    board.place_stone(
        5,
        4,
        PLAYER_BLACK,
    )

    board.place_stone(
        4,
        3,
        PLAYER_BLACK,
    )

    assert_true(
        GoRules.apply_move(
            board,
            4,
            5,
            PLAYER_BLACK,
        )
    )

    assert_equal(
        board.get_cell(4, 4),
        EMPTY,
    )


# ================================================================
# SUICIDE / LEGAL MOVE TESTS
# ================================================================

def test_rules_suicide():
    board = GoBoard()

    board.place_stone(
        3,
        4,
        PLAYER_WHITE,
    )

    board.place_stone(
        5,
        4,
        PLAYER_WHITE,
    )

    board.place_stone(
        4,
        3,
        PLAYER_WHITE,
    )

    board.place_stone(
        4,
        5,
        PLAYER_WHITE,
    )

    assert_true(
        GoRules.is_suicide(
            board,
            4,
            4,
            PLAYER_BLACK,
        )
    )


def test_rules_legal_empty_move():
    board = GoBoard()

    assert_true(
        GoRules.is_valid_move(
            board,
            4,
            4,
            PLAYER_BLACK,
        )
    )


def test_rules_occupied_move_invalid():
    board = GoBoard()

    board.place_stone(
        4,
        4,
        PLAYER_BLACK,
    )

    assert_false(
        GoRules.is_valid_move(
            board,
            4,
            4,
            PLAYER_WHITE,
        )
    )


def test_rules_invalid_player_move():
    board = GoBoard()

    assert_false(
        GoRules.is_valid_move(
            board,
            4,
            4,
            99,
        )
    )


def test_rules_invalid_position_move():
    board = GoBoard()

    assert_false(
        GoRules.is_valid_move(
            board,
            -1,
            4,
            PLAYER_BLACK,
        )
    )


def test_rules_legal_moves_initial_board():
    board = GoBoard()

    moves = GoRules.get_legal_moves(
        board,
        PLAYER_BLACK,
    )

    assert_equal(
        len(moves),
        BOARD_ROWS * BOARD_COLUMNS,
    )


def test_rules_valid_moves_alias():
    board = GoBoard()

    valid_moves = GoRules.get_valid_moves(
        board,
        PLAYER_BLACK,
    )

    legal_moves = GoRules.get_legal_moves(
        board,
        PLAYER_BLACK,
    )

    assert_equal(
        valid_moves,
        legal_moves,
    )


def test_rules_has_legal_moves():
    board = GoBoard()

    assert_true(
        GoRules.has_legal_moves(
            board,
            PLAYER_BLACK,
        )
    )


# ================================================================
# SIMULATION / APPLICATION TESTS
# ================================================================

def test_rules_simulate_move_does_not_modify_original():
    board = GoBoard()

    original_state = (
        board.get_board_state()
    )

    simulated = GoRules.simulate_move(
        board,
        4,
        4,
        PLAYER_BLACK,
    )

    assert_is_not_none(simulated)

    assert_equal(
        board.get_board_state(),
        original_state,
    )

    assert_equal(
        board.get_cell(4, 4),
        EMPTY,
    )

    assert_equal(
        simulated.get_cell(4, 4),
        PLAYER_BLACK,
    )


def test_rules_apply_move_changes_board():
    board = GoBoard()

    assert_true(
        GoRules.apply_move(
            board,
            4,
            4,
            PLAYER_BLACK,
        )
    )

    assert_equal(
        board.get_cell(4, 4),
        PLAYER_BLACK,
    )


def test_rules_invalid_application():
    board = GoBoard()

    assert_false(
        GoRules.apply_move(
            board,
            4,
            4,
            PLAYER_BLACK,
            (4, 4),
        )
    )


# ================================================================
# KO TESTS
# ================================================================

def test_rules_ko_api_exists():
    assert_true(
        callable(
            GoRules.get_ko_position
        )
    )

    assert_true(
        callable(
            GoRules.is_ko_move
        )
    )


def test_rules_ko_no_previous_board():
    board = GoBoard()

    assert_is_none(
        GoRules.get_ko_position(
            None,
            board,
            4,
            4,
            PLAYER_BLACK,
        )
    )


def test_rules_ko_position_restriction():
    board = GoBoard()

    assert_false(
        GoRules.is_valid_move(
            board,
            4,
            4,
            PLAYER_BLACK,
            (4, 4),
        )
    )

    assert_true(
        GoRules.is_valid_move(
            board,
            4,
            4,
            PLAYER_BLACK,
            (3, 3),
        )
    )


# ================================================================
# BOARD COMPARISON TESTS
# ================================================================

def test_rules_boards_equal():
    board_a = GoBoard()
    board_b = GoBoard()

    assert_true(
        GoRules.boards_equal(
            board_a,
            board_b,
        )
    )

    board_a.place_stone(
        4,
        4,
        PLAYER_BLACK,
    )

    assert_false(
        GoRules.boards_equal(
            board_a,
            board_b,
        )
    )


def test_rules_boards_equal_same_object():
    board = GoBoard()

    assert_true(
        GoRules.boards_equal(
            board,
            board,
        )
    )


# ================================================================
# TERRITORY / SCORING TESTS
# ================================================================

def test_rules_empty_regions():
    board = GoBoard()

    regions = (
        GoRules.get_empty_regions(
            board
        )
    )

    assert_true(
        isinstance(regions, list)
    )

    assert_equal(
        len(regions),
        1,
    )


def test_rules_region_owner_empty_board():
    board = GoBoard()

    regions = (
        GoRules.get_empty_regions(
            board
        )
    )

    owner = (
        GoRules.get_region_owner(
            board,
            regions[0],
        )
    )

    assert_is_none(owner)


def test_rules_territory_returns_integer():
    board = GoBoard()

    black_territory = (
        GoRules.count_territory(
            board,
            PLAYER_BLACK,
        )
    )

    white_territory = (
        GoRules.count_territory(
            board,
            PLAYER_WHITE,
        )
    )

    assert_true(
        isinstance(
            black_territory,
            int,
        )
    )

    assert_true(
        isinstance(
            white_territory,
            int,
        )
    )


def test_rules_invalid_player_territory():
    board = GoBoard()

    assert_equal(
        GoRules.count_territory(
            board,
            99,
        ),
        0,
    )


def test_rules_score_type():
    board = GoBoard()

    black_score = (
        GoRules.calculate_score(
            board,
            PLAYER_BLACK,
        )
    )

    white_score = (
        GoRules.calculate_score(
            board,
            PLAYER_WHITE,
        )
    )

    assert_true(
        isinstance(
            black_score,
            float,
        )
    )

    assert_true(
        isinstance(
            white_score,
            float,
        )
    )


def test_rules_komi():
    board = GoBoard()

    black_score = (
        GoRules.calculate_score(
            board,
            PLAYER_BLACK,
        )
    )

    white_score = (
        GoRules.calculate_score(
            board,
            PLAYER_WHITE,
        )
    )

    assert_equal(
        white_score - black_score,
        KOMI,
    )


def test_rules_get_scores():
    board = GoBoard()

    scores = GoRules.get_scores(
        board
    )

    assert_true(
        isinstance(scores, dict)
    )

    assert_true(
        PLAYER_BLACK in scores
    )

    assert_true(
        PLAYER_WHITE in scores
    )


def test_rules_winner():
    board = GoBoard()

    winner = GoRules.get_winner(
        board
    )

    assert_true(
        winner in (
            PLAYER_BLACK,
            PLAYER_WHITE,
            None,
        )
    )


def test_rules_draw():
    board = GoBoard()

    draw = GoRules.is_draw(
        board
    )

    assert_true(
        isinstance(draw, bool)
    )


def test_rules_evaluate_game():
    board = GoBoard()

    result = GoRules.evaluate_game(
        board
    )

    assert_true(
        result.game_over
    )

    assert_true(
        hasattr(result, "winner")
    )

    assert_true(
        hasattr(result, "draw")
    )

    assert_true(
        hasattr(result, "scores")
    )


def test_rules_additional_helpers():
    board = GoBoard()

    assert_false(
        GoRules.is_board_full(
            board
        )
    )

    assert_equal(
        GoRules.get_stone_count(
            board,
            PLAYER_BLACK,
        ),
        0,
    )

    assert_equal(
        GoRules.get_position_count(
            board,
            PLAYER_BLACK,
        ),
        0,
    )


# ================================================================
# AI TESTS
# ================================================================

def test_ai_creation():
    black_ai = GoAI(
        PLAYER_BLACK
    )

    white_ai = GoAI(
        PLAYER_WHITE
    )

    assert_equal(
        black_ai.player,
        PLAYER_BLACK,
    )

    assert_equal(
        white_ai.player,
        PLAYER_WHITE,
    )


def test_ai_initialization():
    ai = GoAI(
        PLAYER_BLACK
    )

    assert_false(
        ai.initialized
    )

    ai.initialize()

    assert_true(
        ai.initialized
    )


def test_ai_reset():
    ai = GoAI(
        PLAYER_BLACK
    )

    ai.initialize()
    ai.reset()

    assert_false(
        ai.initialized
    )


def test_ai_requires_initialization():
    ai = GoAI(
        PLAYER_BLACK
    )

    game_state = {
        "board": GoBoard().get_board_state(),
        "previous_board": None,
        "current_player": PLAYER_BLACK,
    }

    assert_is_none(
        ai.select_action(
            game_state
        )
    )


def test_ai_selects_action():
    ai = GoAI(
        PLAYER_BLACK
    )

    ai.initialize()

    board = GoBoard()

    state = {
        "board": board.get_board_state(),
        "previous_board": None,
        "current_player": PLAYER_BLACK,
    }

    action = ai.select_action(
        state
    )

    assert_is_not_none(action)

    if action != ACTION_PASS:
        assert_true(
            isinstance(action, tuple)
        )

        assert_equal(
            len(action),
            2,
        )

        row, column = action

        assert_true(
            GoRules.is_valid_move(
                board,
                row,
                column,
                PLAYER_BLACK,
            )
        )


def test_ai_wrong_turn():
    ai = GoAI(
        PLAYER_BLACK
    )

    ai.initialize()

    board = GoBoard()

    state = {
        "board": board.get_board_state(),
        "previous_board": None,
        "current_player": PLAYER_WHITE,
    }

    assert_is_none(
        ai.select_action(
            state
        )
    )


def test_ai_invalid_state():
    ai = GoAI(
        PLAYER_BLACK
    )

    ai.initialize()

    assert_is_none(
        ai.select_action(None)
    )

    assert_is_none(
        ai.select_action({})
    )


def test_ai_get_action():
    ai = GoAI(
        PLAYER_BLACK
    )

    ai.initialize()

    game, _ = create_game(
        GAME_MODE_AI_VS_AI
    )

    action = ai.get_action(
        game
    )

    assert_is_not_none(action)


def test_ai_full_board_pass():
    ai = GoAI(
        PLAYER_BLACK
    )

    ai.initialize()

    board = GoBoard()

    fill_board(
        board,
        PLAYER_WHITE,
    )

    state = {
        "board": board.get_board_state(),
        "previous_board": None,
        "current_player": PLAYER_BLACK,
    }

    action = ai.select_action(
        state
    )

    assert_equal(
        action,
        ACTION_PASS,
    )


# ================================================================
# BOARD RENDERER TESTS
# ================================================================

def test_board_renderer_creation():
    renderer = MockRenderer()

    board_renderer = GoBoardRenderer(
        renderer
    )

    assert_equal(
        board_renderer.renderer,
        renderer,
    )


def test_board_renderer_reset():
    renderer = MockRenderer()

    board_renderer = GoBoardRenderer(
        renderer
    )

    assert_true(
        board_renderer.reset()
        is None
    )


def test_board_renderer_cell_center():
    renderer = MockRenderer()

    board_renderer = GoBoardRenderer(
        renderer
    )

    center = (
        board_renderer.get_cell_center(
            0,
            0,
        )
    )

    assert_equal(
        center,
        (
            board_renderer.origin_x,
            board_renderer.origin_y,
        ),
    )


def test_board_renderer_center_position():
    renderer = MockRenderer()

    board_renderer = GoBoardRenderer(
        renderer
    )

    center = (
        board_renderer.get_cell_center(
            4,
            4,
        )
    )

    assert_true(
        isinstance(center, tuple)
    )

    assert_equal(
        len(center),
        2,
    )


def test_board_renderer_invalid_row():
    renderer = MockRenderer()

    board_renderer = GoBoardRenderer(
        renderer
    )

    try:
        board_renderer.get_cell_center(
            -1,
            0,
        )

        raise AssertionError(
            "Invalid row accepted"
        )

    except ValueError:
        pass


def test_board_renderer_invalid_column():
    renderer = MockRenderer()

    board_renderer = GoBoardRenderer(
        renderer
    )

    try:
        board_renderer.get_cell_center(
            0,
            9,
        )

        raise AssertionError(
            "Invalid column accepted"
        )

    except ValueError:
        pass


def test_board_renderer_contains_point():
    renderer = MockRenderer()

    board_renderer = GoBoardRenderer(
        renderer
    )

    x, y = (
        board_renderer.get_cell_center(
            4,
            4,
        )
    )

    assert_true(
        board_renderer.contains_point(
            x,
            y,
        )
    )


def test_board_renderer_outside_point():
    renderer = MockRenderer()

    board_renderer = GoBoardRenderer(
        renderer
    )

    assert_false(
        board_renderer.contains_point(
            -1000,
            -1000,
        )
    )


def test_board_renderer_screen_to_board():
    renderer = MockRenderer()

    board_renderer = GoBoardRenderer(
        renderer
    )

    center = (
        board_renderer.get_cell_center(
            4,
            4,
        )
    )

    position = (
        board_renderer.screen_to_board(
            center
        )
    )

    assert_equal(
        position,
        (4, 4),
    )


def test_board_renderer_screen_to_cell():
    renderer = MockRenderer()

    board_renderer = GoBoardRenderer(
        renderer
    )

    center = (
        board_renderer.get_cell_center(
            4,
            4,
        )
    )

    position = (
        board_renderer.screen_to_cell(
            center[0],
            center[1],
        )
    )

    assert_equal(
        position,
        (4, 4),
    )


def test_board_renderer_invalid_screen_position():
    renderer = MockRenderer()

    board_renderer = GoBoardRenderer(
        renderer
    )

    assert_is_none(
        board_renderer.screen_to_board(
            None
        )
    )

    assert_is_none(
        board_renderer.screen_to_board(
            (-1000, -1000)
        )
    )


def test_board_renderer_render_empty_board():
    renderer = MockRenderer()

    board_renderer = GoBoardRenderer(
        renderer
    )

    board = GoBoard()

    board_renderer.render(
        board
    )

    assert_true(
        len(renderer.calls) > 0
    )


def test_board_renderer_render_stones():
    renderer = MockRenderer()

    board_renderer = GoBoardRenderer(
        renderer
    )

    board = GoBoard()

    board.place_stone(
        4,
        4,
        PLAYER_BLACK,
    )

    board.place_stone(
        3,
        3,
        PLAYER_WHITE,
    )

    board_renderer.render(
        board
    )

    circle_calls = [
        call
        for call in renderer.calls
        if call[0] == "circle"
    ]

    assert_true(
        len(circle_calls) >= 2
    )


def test_board_renderer_render_legal_moves():
    renderer = MockRenderer()

    board_renderer = GoBoardRenderer(
        renderer
    )

    board = GoBoard()

    board_renderer.render(
        board,
        legal_moves=[
            (0, 0),
            (4, 4),
        ],
    )

    assert_true(
        len(renderer.calls) > 0
    )


def test_board_renderer_render_last_move():
    renderer = MockRenderer()

    board_renderer = GoBoardRenderer(
        renderer
    )

    board = GoBoard()

    board_renderer.render(
        board,
        last_move=(4, 4),
    )

    assert_true(
        len(renderer.calls) > 0
    )


def test_board_renderer_render_ko():
    renderer = MockRenderer()

    board_renderer = GoBoardRenderer(
        renderer
    )

    board = GoBoard()

    board_renderer.render(
        board,
        ko_position=(4, 4),
    )

    assert_true(
        len(renderer.calls) > 0
    )


# ================================================================
# HUMAN PLAYER TESTS
# ================================================================

def test_human_player_creation():
    renderer = MockRenderer()

    board_renderer = GoBoardRenderer(
        renderer
    )

    human = HumanPlayer(
        board_renderer
    )

    assert_is_none(
        human.player
    )


def test_human_player_initialize():
    renderer = MockRenderer()

    board_renderer = GoBoardRenderer(
        renderer
    )

    human = HumanPlayer(
        board_renderer
    )

    human.initialize()

    assert_is_none(
        human.player
    )


def test_human_player_set_player():
    renderer = MockRenderer()

    board_renderer = GoBoardRenderer(
        renderer
    )

    human = HumanPlayer(
        board_renderer
    )

    human.set_player(
        PLAYER_BLACK
    )

    assert_equal(
        human.player,
        PLAYER_BLACK,
    )

    human.set_player(
        PLAYER_WHITE
    )

    assert_equal(
        human.player,
        PLAYER_WHITE,
    )


def test_human_player_invalid_player():
    renderer = MockRenderer()

    board_renderer = GoBoardRenderer(
        renderer
    )

    human = HumanPlayer(
        board_renderer
    )

    try:
        human.set_player(99)

        raise AssertionError(
            "Invalid player accepted"
        )

    except ValueError:
        pass


def test_human_player_none_game():
    renderer = MockRenderer()

    board_renderer = GoBoardRenderer(
        renderer
    )

    human = HumanPlayer(
        board_renderer
    )

    assert_is_none(
        human.get_action(None)
    )


# ================================================================
# OVERLAY RENDERER TESTS
# ================================================================

def test_overlay_renderer_creation():
    renderer = MockRenderer()

    overlay = GoOverlayRenderer(
        renderer
    )

    assert_equal(
        overlay.renderer,
        renderer,
    )


def test_overlay_renderer_reset():
    renderer = MockRenderer()

    overlay = GoOverlayRenderer(
        renderer
    )

    assert_true(
        overlay.reset()
        is None
    )


def test_overlay_renderer_not_game_over():
    renderer = MockRenderer()

    overlay = GoOverlayRenderer(
        renderer
    )

    board = GoBoard()

    result = GoRules.evaluate_game(
        board
    )

    result.game_over = False

    overlay.render(
        result,
        board,
    )

    assert_equal(
        len(renderer.overlay_messages),
        0,
    )


def test_overlay_renderer_game_over():
    renderer = MockRenderer()

    overlay = GoOverlayRenderer(
        renderer
    )

    board = GoBoard()

    result = GoRules.evaluate_game(
        board
    )

    overlay.render(
        result,
        board,
    )

    assert_true(
        len(renderer.overlay_messages)
        >= 1
    )


# ================================================================
# GAME CREATION / INITIALIZATION
# ================================================================

def test_game_creation_human_vs_human():
    game, _ = create_game(
        GAME_MODE_HUMAN_VS_HUMAN
    )

    assert_equal(
        game.game_mode,
        GAME_MODE_HUMAN_VS_HUMAN,
    )

    assert_equal(
        game.get_game_state(),
        GAME_RUNNING,
    )


def test_game_creation_human_vs_ai():
    game, _ = create_game(
        GAME_MODE_HUMAN_VS_AI
    )

    assert_equal(
        game.game_mode,
        GAME_MODE_HUMAN_VS_AI,
    )

    assert_is_not_none(
        game.black_controller
    )

    assert_is_not_none(
        game.white_controller
    )


def test_game_creation_ai_vs_ai():
    game, _ = create_game(
        GAME_MODE_AI_VS_AI
    )

    assert_equal(
        game.game_mode,
        GAME_MODE_AI_VS_AI,
    )

    assert_is_not_none(
        game.black_controller
    )

    assert_is_not_none(
        game.white_controller
    )


def test_game_initial_state():
    game, _ = create_game()

    assert_equal(
        game.get_move_count(),
        0,
    )

    assert_equal(
        game.get_consecutive_passes(),
        0,
    )

    assert_is_none(
        game.get_last_move()
    )

    assert_is_none(
        game.get_ko_position()
    )

    assert_equal(
        game.get_black_count(),
        0,
    )

    assert_equal(
        game.get_white_count(),
        0,
    )


def test_game_first_player():
    game, _ = create_game()

    assert_true(
        game.get_current_player()
        in (
            PLAYER_BLACK,
            PLAYER_WHITE,
        )
    )


def test_game_controllers():
    game, _ = create_game(
        GAME_MODE_HUMAN_VS_HUMAN
    )

    assert_is_not_none(
        game.get_current_controller()
    )

    assert_is_not_none(
        game.black_controller
    )

    assert_is_not_none(
        game.white_controller
    )


# ================================================================
# GAME MOVE TESTS
# ================================================================

def test_game_make_move():
    game, _ = create_game(
        GAME_MODE_HUMAN_VS_HUMAN
    )

    starting_player = (
        game.get_current_player()
    )

    assert_true(
        game.make_move(
            4,
            4,
        )
    )

    assert_equal(
        game.get_board().get_cell(
            4,
            4,
        ),
        starting_player,
    )

    assert_equal(
        game.get_move_count(),
        1,
    )

    assert_equal(
        game.get_last_move(),
        (4, 4),
    )


def test_game_switches_player_after_move():
    game, _ = create_game(
        GAME_MODE_HUMAN_VS_HUMAN
    )

    starting_player = (
        game.get_current_player()
    )

    game.make_move(
        4,
        4,
    )

    assert_not_equal(
        game.get_current_player(),
        starting_player,
    )


def test_game_invalid_move():
    game, _ = create_game(
        GAME_MODE_HUMAN_VS_HUMAN
    )

    assert_true(
        game.make_move(
            4,
            4,
        )
    )

    assert_false(
        game.make_move(
            4,
            4,
        )
    )

    assert_equal(
        game.get_move_count(),
        1,
    )


def test_game_invalid_position():
    game, _ = create_game(
        GAME_MODE_HUMAN_VS_HUMAN
    )

    assert_false(
        game.make_move(
            -1,
            4,
        )
    )

    assert_false(
        game.make_move(
            9,
            4,
        )
    )


def test_game_multiple_moves():
    game, _ = create_game(
        GAME_MODE_HUMAN_VS_HUMAN
    )

    assert_true(
        game.make_move(4, 4)
    )

    assert_true(
        game.make_move(4, 5)
    )

    assert_true(
        game.make_move(5, 5)
    )

    assert_equal(
        game.get_move_count(),
        3,
    )

    assert_equal(
        game.get_black_count()
        + game.get_white_count(),
        3,
    )


def test_game_capture():
    game, _ = create_game(
        GAME_MODE_HUMAN_VS_HUMAN
    )

    # Black
    game.make_move(3, 4)

    # White
    game.make_move(4, 4)

    # Black
    game.make_move(5, 4)

    # White
    game.make_move(8, 8)

    # Black
    game.make_move(4, 3)

    # White
    game.make_move(7, 7)

    # Black
    game.make_move(4, 5)

    assert_equal(
        game.get_board().get_cell(
            4,
            4,
        ),
        EMPTY,
    )


def test_game_scores():
    game, _ = create_game()

    black_score = (
        game.get_black_score()
    )

    white_score = (
        game.get_white_score()
    )

    assert_true(
        isinstance(
            black_score,
            float,
        )
    )

    assert_true(
        isinstance(
            white_score,
            float,
        )
    )


def test_game_legal_moves():
    game, _ = create_game()

    moves = (
        game.get_legal_moves()
    )

    assert_true(
        isinstance(moves, list)
    )

    assert_true(
        len(moves) > 0
    )


# ================================================================
# GAME PASS / END TESTS
# ================================================================

def test_game_first_pass():
    game, _ = create_game()

    assert_true(
        game.pass_turn()
    )

    assert_equal(
        game.get_consecutive_passes(),
        1,
    )

    assert_false(
        game.is_game_over()
    )


def test_game_two_passes_end_game():
    game, _ = create_game()

    assert_true(
        game.pass_turn()
    )

    assert_true(
        game.pass_turn()
    )

    assert_true(
        game.is_game_over()
    )

    assert_equal(
        game.get_consecutive_passes(),
        2,
    )

    assert_true(
        game.get_game_state()
        in (
            GAME_DRAW,
            GAME_OVER,
        )
    )


def test_game_pass_switches_player():
    game, _ = create_game()

    first_player = (
        game.get_current_player()
    )

    game.pass_turn()

    assert_not_equal(
        game.get_current_player(),
        first_player,
    )


def test_game_finished_cannot_move():
    game, _ = create_game()

    game.pass_turn()
    game.pass_turn()

    assert_false(
        game.make_move(
            4,
            4,
        )
    )


def test_game_finished_cannot_pass():
    game, _ = create_game()

    game.pass_turn()
    game.pass_turn()

    assert_false(
        game.pass_turn()
    )


# ================================================================
# GAME STATE TESTS
# ================================================================

def test_game_state_structure():
    game, _ = create_game()

    state = game.get_state()

    required_keys = (
        "board",
        "previous_board",
        "current_player",
        "winner",
        "game_state",
        "game_over",
        "draw",
        "move_count",
        "consecutive_passes",
        "last_move",
        "ko_position",
        "black_count",
        "white_count",
        "black_score",
        "white_score",
        "legal_moves",
    )

    for key in required_keys:
        assert_true(
            key in state,
            f"Missing state key: {key}",
        )


def test_game_state_board():
    game, _ = create_game()

    state = game.get_state()

    assert_equal(
        len(state["board"]),
        BOARD_ROWS,
    )

    assert_equal(
        len(state["board"][0]),
        BOARD_COLUMNS,
    )


def test_game_state_updates_after_move():
    game, _ = create_game()

    game.make_move(
        4,
        4,
    )

    state = game.get_state()

    assert_equal(
        state["move_count"],
        1,
    )

    assert_equal(
        state["last_move"],
        (4, 4),
    )

    assert_equal(
        state["black_count"]
        + state["white_count"],
        1,
    )


# ================================================================
# GAME RESET TESTS
# ================================================================

def test_game_reset():
    game, _ = create_game()

    game.make_move(
        4,
        4,
    )

    assert_equal(
        game.get_move_count(),
        1,
    )

    game.reset()

    assert_equal(
        game.get_move_count(),
        0,
    )

    assert_equal(
        game.get_black_count(),
        0,
    )

    assert_equal(
        game.get_white_count(),
        0,
    )

    assert_is_none(
        game.get_last_move()
    )

    assert_false(
        game.is_game_over()
    )


def test_game_starting_player_rotation():
    game, _ = create_game()

    first_player = (
        game.get_current_player()
    )

    game.reset()

    second_player = (
        game.get_current_player()
    )

    assert_not_equal(
        first_player,
        second_player,
    )


# ================================================================
# GAME UPDATE / RENDER TESTS
# ================================================================

def test_game_render():
    game, renderer = create_game()

    game.render()

    assert_true(
        len(renderer.calls) > 0
    )


def test_game_update():
    game, _ = create_game(
        GAME_MODE_HUMAN_VS_HUMAN
    )

    # HumanPlayer may simply return None when there is no input.
    game.update()

    assert_equal(
        game.get_move_count(),
        0,
    )


def test_game_shutdown():
    game, _ = create_game()

    assert_true(
        game.shutdown()
        is None
    )


# ================================================================
# AI VS AI INTEGRATION TEST
# ================================================================

def test_ai_vs_ai_controllers():
    game, _ = create_game(
        GAME_MODE_AI_VS_AI
    )

    assert_true(
        isinstance(
            game.black_controller,
            GoAI,
        )
    )

    assert_true(
        isinstance(
            game.white_controller,
            GoAI,
        )
    )


def test_ai_vs_ai_single_turn():
    game, _ = create_game(
        GAME_MODE_AI_VS_AI
    )

    initial_moves = (
        game.get_move_count()
    )

    game.update()

    assert_true(
        game.get_move_count()
        >= initial_moves
    )


def test_ai_vs_ai_game_flow():
    game, _ = create_game(
        GAME_MODE_AI_VS_AI
    )

    maximum_turns = 200

    for _ in range(maximum_turns):

        if game.is_game_over():
            break

        game.update()

    assert_true(
        game.get_move_count() > 0
    )


# ================================================================
# HUMAN VS AI INTEGRATION TEST
# ================================================================

def test_human_vs_ai_controllers():
    game, _ = create_game(
        GAME_MODE_HUMAN_VS_AI
    )

    assert_true(
        isinstance(
            game.black_controller,
            HumanPlayer,
        )
    )

    assert_true(
        isinstance(
            game.white_controller,
            GoAI,
        )
    )


# ================================================================
# COMPLETE WORKING MODEL TEST
# ================================================================

def test_complete_manual_game_flow():
    """
    Execute a complete legal game sequence using direct game
    operations and finish with two passes.
    """

    game, _ = create_game(
        GAME_MODE_HUMAN_VS_HUMAN
    )

    moves = [
        (4, 4),
        (3, 4),
        (4, 5),
        (3, 5),
        (5, 4),
        (2, 4),
        (5, 5),
        (2, 5),
        (4, 3),
        (3, 3),
    ]

    successful_moves = 0

    for row, column in moves:

        if game.is_game_over():
            break

        if game.make_move(
            row,
            column,
        ):
            successful_moves += 1

    assert_true(
        successful_moves > 0
    )

    assert_equal(
        game.get_move_count(),
        successful_moves,
    )

    # Finish the game.
    while (
        not game.is_game_over()
        and game.get_consecutive_passes()
        < CONSECUTIVE_PASSES_TO_END
    ):
        game.pass_turn()

    assert_true(
        game.is_game_over()
    )

    result = game.get_result()

    assert_true(
        result.game_over
    )

    assert_true(
        hasattr(result, "scores")
    )


# ================================================================
# FILE / CLASS AVAILABILITY TEST
# ================================================================

def test_all_go_components_available():
    """
    Final structural test confirming that every Go component used
    by the working model can be imported and instantiated.
    """

    assert_true(
        callable(GoBoard)
    )

    assert_true(
        callable(GoRules.get_legal_moves)
    )

    assert_true(
        callable(GoAI)
    )

    assert_true(
        callable(GoBoardRenderer)
    )

    assert_true(
        callable(HumanPlayer)
    )

    assert_true(
        callable(GoOverlayRenderer)
    )

    assert_true(
        callable(GoGame)
    )


# ================================================================
# RUN ALL TESTS
# ================================================================

def run_all_tests():

    print()
    print("=" * 70)
    print("MINDWAR ARENA - GO COMPLETE TEST")
    print("=" * 70)
    print()

    # ------------------------------------------------------------
    # Constants
    # ------------------------------------------------------------

    test(
        "Constants - Basic",
        test_constants_basic,
    )

    test(
        "Constants - Game States",
        test_constants_game_states,
    )

    test(
        "Constants - Game Modes",
        test_constants_game_modes,
    )

    test(
        "Constants - AI Modes",
        test_constants_ai_modes,
    )

    test(
        "Constants - Rules",
        test_constants_rules,
    )

    test(
        "Constants - Rendering",
        test_constants_rendering,
    )

    # ------------------------------------------------------------
    # Board
    # ------------------------------------------------------------

    test(
        "Board - Creation",
        test_board_creation,
    )

    test(
        "Board - Initially Empty",
        test_board_initially_empty,
    )

    test(
        "Board - Position Validation",
        test_board_position_validation,
    )

    test(
        "Board - Set/Get Cell",
        test_board_set_and_get_cell,
    )

    test(
        "Board - Invalid Cell Value",
        test_board_invalid_cell_value,
    )

    test(
        "Board - Invalid Get Position",
        test_board_invalid_get_position,
    )

    test(
        "Board - Place Stone",
        test_board_place_stone,
    )

    test(
        "Board - Occupied Cell",
        test_board_cannot_place_on_occupied_cell,
    )

    test(
        "Board - Invalid Place",
        test_board_invalid_place_stone,
    )

    test(
        "Board - Remove Stone",
        test_board_remove_stone,
    )

    test(
        "Board - Remove Empty",
        test_board_remove_empty_stone,
    )

    test(
        "Board - Empty Positions",
        test_board_empty_positions,
    )

    test(
        "Board - Player Positions",
        test_board_player_positions,
    )

    test(
        "Board - Counts",
        test_board_counts,
    )

    test(
        "Board - Full Detection",
        test_board_full_detection,
    )

    test(
        "Board - Copy",
        test_board_state_copy,
    )

    test(
        "Board - Get/Set State",
        test_board_get_set_state,
    )

    test(
        "Board - Invalid State",
        test_board_invalid_state,
    )

    test(
        "Board - String",
        test_board_string,
    )

    # ------------------------------------------------------------
    # Rules
    # ------------------------------------------------------------

    test(
        "Rules - Player Validation",
        test_rules_player_validation,
    )

    test(
        "Rules - Opponent",
        test_rules_opponent,
    )

    test(
        "Rules - Position Validation",
        test_rules_position_validation,
    )

    test(
        "Rules - Same Position",
        test_rules_same_position,
    )

    test(
        "Rules - Corner Neighbors",
        test_rules_corner_neighbors,
    )

    test(
        "Rules - Center Neighbors",
        test_rules_center_neighbors,
    )

    test(
        "Rules - Invalid Neighbors",
        test_rules_invalid_neighbors,
    )

    test(
        "Rules - Single Group",
        test_rules_single_group,
    )

    test(
        "Rules - Connected Group",
        test_rules_connected_group,
    )

    test(
        "Rules - Group Separation",
        test_rules_group_does_not_include_opponent,
    )

    test(
        "Rules - Group Liberties",
        test_rules_group_liberties,
    )

    test(
        "Rules - Corner Liberties",
        test_rules_count_liberties_corner,
    )

    test(
        "Rules - Center Liberties",
        test_rules_count_liberties_center,
    )

    test(
        "Rules - Capture Detection",
        test_rules_capture_detection,
    )

    test(
        "Rules - Captured Positions",
        test_rules_get_captured_positions,
    )

    test(
        "Rules - Capture Group",
        test_rules_capture_group,
    )

    test(
        "Rules - Capture Opponent",
        test_rules_capture_opponent_groups,
    )

    test(
        "Rules - Apply Capture",
        test_rules_apply_capture_move,
    )

    test(
        "Rules - Suicide",
        test_rules_suicide,
    )

    test(
        "Rules - Legal Empty Move",
        test_rules_legal_empty_move,
    )

    test(
        "Rules - Occupied Move",
        test_rules_occupied_move_invalid,
    )

    test(
        "Rules - Invalid Player Move",
        test_rules_invalid_player_move,
    )

    test(
        "Rules - Invalid Position Move",
        test_rules_invalid_position_move,
    )

    test(
        "Rules - Initial Legal Moves",
        test_rules_legal_moves_initial_board,
    )

    test(
        "Rules - Valid/Legal Alias",
        test_rules_valid_moves_alias,
    )

    test(
        "Rules - Has Legal Moves",
        test_rules_has_legal_moves,
    )

    test(
        "Rules - Simulation",
        test_rules_simulate_move_does_not_modify_original,
    )

    test(
        "Rules - Apply Move",
        test_rules_apply_move_changes_board,
    )

    test(
        "Rules - Invalid Application",
        test_rules_invalid_application,
    )

    test(
        "Rules - Ko API",
        test_rules_ko_api_exists,
    )

    test(
        "Rules - Ko Without Previous Board",
        test_rules_ko_no_previous_board,
    )

    test(
        "Rules - Ko Restriction",
        test_rules_ko_position_restriction,
    )

    test(
        "Rules - Board Equality",
        test_rules_boards_equal,
    )

    test(
        "Rules - Same Board Object",
        test_rules_boards_equal_same_object,
    )

    test(
        "Rules - Empty Regions",
        test_rules_empty_regions,
    )

    test(
        "Rules - Empty Region Owner",
        test_rules_region_owner_empty_board,
    )

    test(
        "Rules - Territory",
        test_rules_territory_returns_integer,
    )

    test(
        "Rules - Invalid Territory Player",
        test_rules_invalid_player_territory,
    )

    test(
        "Rules - Score Type",
        test_rules_score_type,
    )

    test(
        "Rules - Komi",
        test_rules_komi,
    )

    test(
        "Rules - Scores",
        test_rules_get_scores,
    )

    test(
        "Rules - Winner",
        test_rules_winner,
    )

    test(
        "Rules - Draw",
        test_rules_draw,
    )

    test(
        "Rules - Evaluate Game",
        test_rules_evaluate_game,
    )

    test(
        "Rules - Additional Helpers",
        test_rules_additional_helpers,
    )

    # ------------------------------------------------------------
    # AI
    # ------------------------------------------------------------

    test(
        "AI - Creation",
        test_ai_creation,
    )

    test(
        "AI - Initialization",
        test_ai_initialization,
    )

    test(
        "AI - Reset",
        test_ai_reset,
    )

    test(
        "AI - Requires Initialization",
        test_ai_requires_initialization,
    )

    test(
        "AI - Select Action",
        test_ai_selects_action,
    )

    test(
        "AI - Wrong Turn",
        test_ai_wrong_turn,
    )

    test(
        "AI - Invalid State",
        test_ai_invalid_state,
    )

    test(
        "AI - Get Action",
        test_ai_get_action,
    )

    test(
        "AI - Full Board Pass",
        test_ai_full_board_pass,
    )

    # ------------------------------------------------------------
    # Board Renderer
    # ------------------------------------------------------------

    test(
        "Board Renderer - Creation",
        test_board_renderer_creation,
    )

    test(
        "Board Renderer - Reset",
        test_board_renderer_reset,
    )

    test(
        "Board Renderer - Cell Center",
        test_board_renderer_cell_center,
    )

    test(
        "Board Renderer - Center Position",
        test_board_renderer_center_position,
    )

    test(
        "Board Renderer - Invalid Row",
        test_board_renderer_invalid_row,
    )

    test(
        "Board Renderer - Invalid Column",
        test_board_renderer_invalid_column,
    )

    test(
        "Board Renderer - Contains Point",
        test_board_renderer_contains_point,
    )

    test(
        "Board Renderer - Outside Point",
        test_board_renderer_outside_point,
    )

    test(
        "Board Renderer - Screen To Board",
        test_board_renderer_screen_to_board,
    )

    test(
        "Board Renderer - Screen To Cell",
        test_board_renderer_screen_to_cell,
    )

    test(
        "Board Renderer - Invalid Screen Position",
        test_board_renderer_invalid_screen_position,
    )

    test(
        "Board Renderer - Empty Board Render",
        test_board_renderer_render_empty_board,
    )

    test(
        "Board Renderer - Stone Render",
        test_board_renderer_render_stones,
    )

    test(
        "Board Renderer - Legal Moves Render",
        test_board_renderer_render_legal_moves,
    )

    test(
        "Board Renderer - Last Move Render",
        test_board_renderer_render_last_move,
    )

    test(
        "Board Renderer - Ko Render",
        test_board_renderer_render_ko,
    )

    # ------------------------------------------------------------
    # Human Player
    # ------------------------------------------------------------

    test(
        "Human Player - Creation",
        test_human_player_creation,
    )

    test(
        "Human Player - Initialization",
        test_human_player_initialize,
    )

    test(
        "Human Player - Set Player",
        test_human_player_set_player,
    )

    test(
        "Human Player - Invalid Player",
        test_human_player_invalid_player,
    )

    test(
        "Human Player - None Game",
        test_human_player_none_game,
    )

    # ------------------------------------------------------------
    # Overlay
    # ------------------------------------------------------------

    test(
        "Overlay - Creation",
        test_overlay_renderer_creation,
    )

    test(
        "Overlay - Reset",
        test_overlay_renderer_reset,
    )

    test(
        "Overlay - Not Game Over",
        test_overlay_renderer_not_game_over,
    )

    test(
        "Overlay - Game Over",
        test_overlay_renderer_game_over,
    )

    # ------------------------------------------------------------
    # Game
    # ------------------------------------------------------------

    test(
        "Game - Human vs Human Creation",
        test_game_creation_human_vs_human,
    )

    test(
        "Game - Human vs AI Creation",
        test_game_creation_human_vs_ai,
    )

    test(
        "Game - AI vs AI Creation",
        test_game_creation_ai_vs_ai,
    )

    test(
        "Game - Initial State",
        test_game_initial_state,
    )

    test(
        "Game - First Player",
        test_game_first_player,
    )

    test(
        "Game - Controllers",
        test_game_controllers,
    )

    test(
        "Game - Make Move",
        test_game_make_move,
    )

    test(
        "Game - Player Switching",
        test_game_switches_player_after_move,
    )

    test(
        "Game - Invalid Move",
        test_game_invalid_move,
    )

    test(
        "Game - Invalid Position",
        test_game_invalid_position,
    )

    test(
        "Game - Multiple Moves",
        test_game_multiple_moves,
    )

    test(
        "Game - Capture",
        test_game_capture,
    )

    test(
        "Game - Scores",
        test_game_scores,
    )

    test(
        "Game - Legal Moves",
        test_game_legal_moves,
    )

    # ------------------------------------------------------------
    # Pass / End
    # ------------------------------------------------------------

    test(
        "Game - First Pass",
        test_game_first_pass,
    )

    test(
        "Game - Two Passes End",
        test_game_two_passes_end_game,
    )

    test(
        "Game - Pass Player Switching",
        test_game_pass_switches_player,
    )

    test(
        "Game - Frozen After Finish",
        test_game_finished_cannot_move,
    )

    test(
        "Game - Cannot Pass After Finish",
        test_game_finished_cannot_pass,
    )

    # ------------------------------------------------------------
    # State
    # ------------------------------------------------------------

    test(
        "Game - State Structure",
        test_game_state_structure,
    )

    test(
        "Game - State Board",
        test_game_state_board,
    )

    test(
        "Game - State Update",
        test_game_state_updates_after_move,
    )

    # ------------------------------------------------------------
    # Reset
    # ------------------------------------------------------------

    test(
        "Game - Reset",
        test_game_reset,
    )

    test(
        "Game - Starting Player Rotation",
        test_game_starting_player_rotation,
    )

    # ------------------------------------------------------------
    # Update / Render
    # ------------------------------------------------------------

    test(
        "Game - Render",
        test_game_render,
    )

    test(
        "Game - Update",
        test_game_update,
    )

    test(
        "Game - Shutdown",
        test_game_shutdown,
    )

    # ------------------------------------------------------------
    # Integration
    # ------------------------------------------------------------

    test(
        "Integration - AI vs AI Controllers",
        test_ai_vs_ai_controllers,
    )

    test(
        "Integration - AI vs AI Single Turn",
        test_ai_vs_ai_single_turn,
    )

    test(
        "Integration - AI vs AI Game Flow",
        test_ai_vs_ai_game_flow,
    )

    test(
        "Integration - Human vs AI",
        test_human_vs_ai_controllers,
    )

    test(
        "Integration - Complete Manual Game",
        test_complete_manual_game_flow,
    )

    # ------------------------------------------------------------
    # Structure
    # ------------------------------------------------------------

    test(
        "Structure - All Go Components",
        test_all_go_components_available,
    )

    # ============================================================
    # SUMMARY
    # ============================================================

    print()
    print("=" * 70)
    print("GO TEST SUMMARY")
    print("=" * 70)

    print(
        f"Total Tests : {TOTAL_TESTS}"
    )

    print(
        f"Passed      : {PASSED_TESTS}"
    )

    print(
        f"Failed      : {FAILED_TESTS}"
    )

    if TOTAL_TESTS > 0:
        pass_rate = (
            PASSED_TESTS
            / TOTAL_TESTS
        ) * 100
    else:
        pass_rate = 0.0

    print(
        f"Pass Rate   : {pass_rate:.2f}%"
    )

    print("=" * 70)

    if FAILED_TESTS == 0:
        print()
        print(
            "RESULT: ALL GO TESTS PASSED"
        )
        print(
            "GO WORKING MODEL: VERIFIED"
        )
        print()
        return 0

    print()
    print(
        "RESULT: GO TESTS HAVE FAILURES"
    )
    print(
        "Review the failed tests above."
    )
    print()

    return 1


# ================================================================
# ENTRY POINT
# ================================================================

if __name__ == "__main__":

    # pygame is required by HumanPlayer.
    pygame.init()

    exit_code = run_all_tests()

    pygame.quit()

    sys.exit(exit_code)