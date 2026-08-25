from games.gomoku.board import GomokuBoard
from games.gomoku.constants import (
    BOARD_ROWS,
    BOARD_COLUMNS,
    EMPTY,
    PLAYER_BLACK,
    PLAYER_WHITE,
    WIN_LENGTH,
)
from games.gomoku.rules import GomokuRules


passed = 0
failed = 0


def run_test(name, test_function):
    global passed, failed

    try:
        test_function()
        print(f"[PASS] {name}")
        passed += 1
    except Exception as exception:
        print(f"[FAIL] {name}")
        print(f"       {exception}")
        failed += 1


def create_board(cells):
    board = GomokuBoard()

    for row, column, player in cells:
        board.set_cell(row, column, player)

    return board


# ============================================================
# BOARD TESTS
# ============================================================

def test_board_initialization():
    board = GomokuBoard()

    for row in range(BOARD_ROWS):
        for column in range(BOARD_COLUMNS):
            assert board.get_cell(row, column) == EMPTY


def test_set_cell():
    board = GomokuBoard()

    assert board.set_cell(0, 0, PLAYER_BLACK) is True
    assert board.get_cell(0, 0) == PLAYER_BLACK


def test_invalid_position():
    board = GomokuBoard()

    assert board.is_valid_position(-1, 0) is False
    assert board.is_valid_position(0, -1) is False
    assert board.is_valid_position(BOARD_ROWS, 0) is False
    assert board.is_valid_position(0, BOARD_COLUMNS) is False


def test_occupied_cell():
    board = GomokuBoard()

    board.set_cell(0, 0, PLAYER_BLACK)

    assert board.is_cell_empty(0, 0) is False


def test_available_moves():
    board = GomokuBoard()

    moves = board.get_available_moves()

    assert len(moves) == BOARD_ROWS * BOARD_COLUMNS

    board.set_cell(0, 0, PLAYER_BLACK)

    moves = board.get_available_moves()

    assert len(moves) == (BOARD_ROWS * BOARD_COLUMNS) - 1
    assert (0, 0) not in moves


def test_board_copy():
    board = GomokuBoard()

    board.set_cell(2, 3, PLAYER_BLACK)

    copied_board = board.copy()

    assert copied_board.get_cell(2, 3) == PLAYER_BLACK

    copied_board.set_cell(2, 4, PLAYER_WHITE)

    assert board.get_cell(2, 4) == EMPTY


def test_board_state_is_independent():
    board = GomokuBoard()

    board.set_cell(1, 1, PLAYER_BLACK)

    state = board.get_board_state()

    state[1][1] = PLAYER_WHITE

    assert board.get_cell(1, 1) == PLAYER_BLACK


# ============================================================
# RULE TESTS
# ============================================================

def test_no_winner():
    board = GomokuBoard()

    assert GomokuRules.check_winner(board) == EMPTY


def test_horizontal_win():
    board = create_board([
        (5, 0, PLAYER_BLACK),
        (5, 1, PLAYER_BLACK),
        (5, 2, PLAYER_BLACK),
        (5, 3, PLAYER_BLACK),
        (5, 4, PLAYER_BLACK),
    ])

    assert GomokuRules.check_winner(board) == PLAYER_BLACK


def test_vertical_win():
    board = create_board([
        (0, 3, PLAYER_WHITE),
        (1, 3, PLAYER_WHITE),
        (2, 3, PLAYER_WHITE),
        (3, 3, PLAYER_WHITE),
        (4, 3, PLAYER_WHITE),
    ])

    assert GomokuRules.check_winner(board) == PLAYER_WHITE


def test_diagonal_down_right_win():
    board = create_board([
        (0, 0, PLAYER_BLACK),
        (1, 1, PLAYER_BLACK),
        (2, 2, PLAYER_BLACK),
        (3, 3, PLAYER_BLACK),
        (4, 4, PLAYER_BLACK),
    ])

    assert GomokuRules.check_winner(board) == PLAYER_BLACK


def test_diagonal_down_left_win():
    board = create_board([
        (0, 4, PLAYER_WHITE),
        (1, 3, PLAYER_WHITE),
        (2, 2, PLAYER_WHITE),
        (3, 1, PLAYER_WHITE),
        (4, 0, PLAYER_WHITE),
    ])

    assert GomokuRules.check_winner(board) == PLAYER_WHITE


def test_four_in_a_row_is_not_win():
    board = create_board([
        (5, 0, PLAYER_BLACK),
        (5, 1, PLAYER_BLACK),
        (5, 2, PLAYER_BLACK),
        (5, 3, PLAYER_BLACK),
    ])

    assert GomokuRules.check_winner(board) == EMPTY


def test_separated_stones_are_not_win():
    board = create_board([
        (5, 0, PLAYER_BLACK),
        (5, 1, PLAYER_BLACK),
        (5, 3, PLAYER_BLACK),
        (5, 4, PLAYER_BLACK),
    ])

    assert GomokuRules.check_winner(board) == EMPTY


def test_six_in_a_row_is_win():
    board = create_board([
        (5, 0, PLAYER_BLACK),
        (5, 1, PLAYER_BLACK),
        (5, 2, PLAYER_BLACK),
        (5, 3, PLAYER_BLACK),
        (5, 4, PLAYER_BLACK),
        (5, 5, PLAYER_BLACK),
    ])

    assert GomokuRules.check_winner(board) == PLAYER_BLACK


def test_winning_cells():
    board = create_board([
        (5, 0, PLAYER_BLACK),
        (5, 1, PLAYER_BLACK),
        (5, 2, PLAYER_BLACK),
        (5, 3, PLAYER_BLACK),
        (5, 4, PLAYER_BLACK),
    ])

    winning_cells = GomokuRules.get_winning_cells(board)

    assert len(winning_cells) >= WIN_LENGTH

    for column in range(5):
        assert (5, column) in winning_cells


def test_game_over_after_win():
    board = create_board([
        (5, 0, PLAYER_BLACK),
        (5, 1, PLAYER_BLACK),
        (5, 2, PLAYER_BLACK),
        (5, 3, PLAYER_BLACK),
        (5, 4, PLAYER_BLACK),
    ])

    assert GomokuRules.is_game_over(board) is True


def test_game_not_over_with_four():
    board = create_board([
        (5, 0, PLAYER_BLACK),
        (5, 1, PLAYER_BLACK),
        (5, 2, PLAYER_BLACK),
        (5, 3, PLAYER_BLACK),
    ])

    assert GomokuRules.is_game_over(board) is False


def test_evaluate_game():
    board = create_board([
        (5, 0, PLAYER_BLACK),
        (5, 1, PLAYER_BLACK),
        (5, 2, PLAYER_BLACK),
        (5, 3, PLAYER_BLACK),
        (5, 4, PLAYER_BLACK),
    ])

    result = GomokuRules.evaluate_game(board)

    assert result.game_over is True
    assert result.draw is False
    assert result.winner == PLAYER_BLACK
    assert len(result.winning_cells) >= WIN_LENGTH


# ============================================================
# TEST LIST
# ============================================================

tests = [
    ("Board Initialization", test_board_initialization),
    ("Set Cell", test_set_cell),
    ("Invalid Position", test_invalid_position),
    ("Occupied Cell", test_occupied_cell),
    ("Available Moves", test_available_moves),
    ("Board Copy", test_board_copy),
    ("Board State Independence", test_board_state_is_independent),

    ("No Winner", test_no_winner),
    ("Horizontal Win", test_horizontal_win),
    ("Vertical Win", test_vertical_win),
    ("Diagonal Down-Right Win", test_diagonal_down_right_win),
    ("Diagonal Down-Left Win", test_diagonal_down_left_win),
    ("Four In A Row Is Not Win", test_four_in_a_row_is_not_win),
    ("Separated Stones Are Not Win", test_separated_stones_are_not_win),
    ("Six In A Row Is Win", test_six_in_a_row_is_win),
    ("Winning Cells", test_winning_cells),
    ("Game Over After Win", test_game_over_after_win),
    ("Game Not Over With Four", test_game_not_over_with_four),
    ("Evaluate Game", test_evaluate_game),
]


# ============================================================
# RUN
# ============================================================

print("=" * 60)
print("MINDWAR ARENA - GOMOKU TESTS")
print("=" * 60)

for name, function in tests:
    run_test(name, function)

print()
print("=" * 60)
print("TEST SUMMARY")
print("=" * 60)
print(f"Passed : {passed}")
print(f"Failed : {failed}")
print(f"Total  : {passed + failed}")

if failed == 0:
    print()
    print("ALL GOMOKU TESTS PASSED.")
else:
    print()
    print("SOME GOMOKU TESTS FAILED.")