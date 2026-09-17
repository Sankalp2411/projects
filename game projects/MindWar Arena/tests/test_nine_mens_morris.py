"""
Nine Men's Morris Test Suite

Run:
    python -m tests.test_nine_mens_morris
"""

from games.nine_mens_morris.board import NineMensMorrisBoard
from games.nine_mens_morris.rules import NineMensMorrisRules

from games.nine_mens_morris.constants import (
    BOARD_POSITIONS,
    EMPTY,
    PLAYER_BLACK,
    PLAYER_WHITE,
    PIECES_PER_PLAYER,
    PHASE_PLACEMENT,
    PHASE_MOVEMENT,
)


# ============================================================
# TEST HELPER
# ============================================================

def assert_test(condition, message):
    assert condition, message


def create_empty_board():
    return NineMensMorrisBoard()


def set_positions(board, player, positions):
    for position in positions:
        result = board.set_position(position, player)

        assert_test(
            result is True,
            f"Failed to place player {player} at position {position}"
        )


# ============================================================
# BOARD INITIALIZATION
# ============================================================

def test_board_initialization():
    board = create_empty_board()

    assert_test(
        len(board.get_board_state()) == BOARD_POSITIONS,
        "Board should contain 24 positions"
    )

    for position in range(BOARD_POSITIONS):
        assert_test(
            board.get_position(position) == EMPTY,
            f"Position {position} should initially be empty"
        )


# ============================================================
# POSITION VALIDATION
# ============================================================

def test_valid_positions():
    board = create_empty_board()

    assert_test(
        board.is_valid_position(0),
        "Position 0 should be valid"
    )

    assert_test(
        board.is_valid_position(BOARD_POSITIONS - 1),
        "Last board position should be valid"
    )


def test_invalid_positions():
    board = create_empty_board()

    assert_test(
        not board.is_valid_position(-1),
        "Negative position should be invalid"
    )

    assert_test(
        not board.is_valid_position(BOARD_POSITIONS),
        "Position after the board should be invalid"
    )


# ============================================================
# PIECE PLACEMENT
# ============================================================

def test_place_black_piece():
    board = create_empty_board()

    result = board.place_piece(0, PLAYER_BLACK)

    assert_test(
        result is True,
        "Black piece should be placed successfully"
    )

    assert_test(
        board.get_position(0) == PLAYER_BLACK,
        "Position 0 should contain black piece"
    )


def test_place_white_piece():
    board = create_empty_board()

    result = board.place_piece(10, PLAYER_WHITE)

    assert_test(
        result is True,
        "White piece should be placed successfully"
    )

    assert_test(
        board.get_position(10) == PLAYER_WHITE,
        "Position 10 should contain white piece"
    )


def test_cannot_place_on_occupied_position():
    board = create_empty_board()

    board.place_piece(0, PLAYER_BLACK)

    result = board.place_piece(0, PLAYER_WHITE)

    assert_test(
        result is False,
        "Cannot place a piece on an occupied position"
    )

    assert_test(
        board.get_position(0) == PLAYER_BLACK,
        "Original piece should remain"
    )


def test_invalid_player_cannot_place():
    board = create_empty_board()

    result = board.place_piece(0, 99)

    assert_test(
        result is False,
        "Invalid player should not be allowed"
    )


# ============================================================
# PIECE REMOVAL
# ============================================================

def test_remove_piece():
    board = create_empty_board()

    board.place_piece(0, PLAYER_BLACK)

    result = board.remove_piece(0)

    assert_test(
        result is True,
        "Piece should be removed successfully"
    )

    assert_test(
        board.get_position(0) == EMPTY,
        "Position should be empty after removal"
    )


def test_remove_empty_position():
    board = create_empty_board()

    result = board.remove_piece(0)

    assert_test(
        result is False,
        "Removing an empty position should fail"
    )


# ============================================================
# PIECE MOVEMENT
# ============================================================

def test_move_piece():
    board = create_empty_board()

    board.place_piece(0, PLAYER_BLACK)

    result = board.move_piece(
        0,
        1,
        PLAYER_BLACK
    )

    assert_test(
        result is True,
        "Piece should move successfully"
    )

    assert_test(
        board.get_position(0) == EMPTY,
        "Source position should become empty"
    )

    assert_test(
        board.get_position(1) == PLAYER_BLACK,
        "Destination should contain black piece"
    )


def test_move_wrong_player_piece():
    board = create_empty_board()

    board.place_piece(0, PLAYER_BLACK)

    result = board.move_piece(
        0,
        1,
        PLAYER_WHITE
    )

    assert_test(
        result is False,
        "Player should not move opponent's piece"
    )


def test_move_to_occupied_position():
    board = create_empty_board()

    board.place_piece(0, PLAYER_BLACK)
    board.place_piece(1, PLAYER_WHITE)

    result = board.move_piece(
        0,
        1,
        PLAYER_BLACK
    )

    assert_test(
        result is False,
        "Cannot move onto occupied position"
    )


# ============================================================
# BOARD INFORMATION
# ============================================================

def test_available_positions():
    board = create_empty_board()

    board.place_piece(0, PLAYER_BLACK)
    board.place_piece(1, PLAYER_WHITE)

    available = board.get_available_positions()

    assert_test(
        0 not in available,
        "Occupied position 0 should not be available"
    )

    assert_test(
        1 not in available,
        "Occupied position 1 should not be available"
    )

    assert_test(
        len(available) == BOARD_POSITIONS - 2,
        "There should be 22 available positions"
    )


def test_player_positions():
    board = create_empty_board()

    set_positions(
        board,
        PLAYER_BLACK,
        [0, 1, 2]
    )

    positions = board.get_player_positions(
        PLAYER_BLACK
    )

    assert_test(
        positions == [0, 1, 2],
        "Black positions should be [0, 1, 2]"
    )


def test_piece_count():
    board = create_empty_board()

    set_positions(
        board,
        PLAYER_BLACK,
        [0, 1, 2]
    )

    set_positions(
        board,
        PLAYER_WHITE,
        [3, 4]
    )

    assert_test(
        board.count_pieces(PLAYER_BLACK) == 3,
        "Black should have 3 pieces"
    )

    assert_test(
        board.count_pieces(PLAYER_WHITE) == 2,
        "White should have 2 pieces"
    )


def test_empty_count():
    board = create_empty_board()

    board.place_piece(0, PLAYER_BLACK)

    assert_test(
        board.get_empty_count() == BOARD_POSITIONS - 1,
        "There should be 23 empty positions"
    )


def test_board_full():
    board = create_empty_board()

    for position in range(BOARD_POSITIONS):
        player = (
            PLAYER_BLACK
            if position % 2 == 0
            else PLAYER_WHITE
        )

        board.set_position(
            position,
            player
        )

    assert_test(
        board.is_board_full(),
        "Board should be full"
    )


# ============================================================
# BOARD COPY
# ============================================================

def test_board_copy():
    board = create_empty_board()

    board.place_piece(
        0,
        PLAYER_BLACK
    )

    copied_board = board.copy()

    assert_test(
        copied_board.get_position(0) == PLAYER_BLACK,
        "Copied board should contain original piece"
    )

    copied_board.set_position(
        1,
        PLAYER_WHITE
    )

    assert_test(
        board.get_position(1) == EMPTY,
        "Original board should not change"
    )


# ============================================================
# ADJACENCY
# ============================================================

def test_position_adjacency():
    assert_test(
        NineMensMorrisRules.are_adjacent(0, 1),
        "0 and 1 should be adjacent"
    )

    assert_test(
        NineMensMorrisRules.are_adjacent(0, 9),
        "0 and 9 should be adjacent"
    )


def test_non_adjacent_positions():
    assert_test(
        not NineMensMorrisRules.are_adjacent(0, 2),
        "0 and 2 should not be adjacent"
    )


def test_get_adjacent_positions():
    neighbors = NineMensMorrisRules.get_adjacent_positions(0)

    assert_test(
        1 in neighbors,
        "Position 1 should be adjacent to 0"
    )

    assert_test(
        9 in neighbors,
        "Position 9 should be adjacent to 0"
    )


# ============================================================
# MILL TESTS
# ============================================================

def test_horizontal_mill():
    board = create_empty_board()

    set_positions(
        board,
        PLAYER_BLACK,
        [0, 1, 2]
    )

    assert_test(
        NineMensMorrisRules.is_mill(
            board,
            1,
            PLAYER_BLACK
        ),
        "0-1-2 should form a mill"
    )


def test_vertical_mill():
    board = create_empty_board()

    set_positions(
        board,
        PLAYER_BLACK,
        [0, 9, 21]
    )

    assert_test(
        NineMensMorrisRules.is_mill(
            board,
            9,
            PLAYER_BLACK
        ),
        "0-9-21 should form a mill"
    )


def test_incomplete_mill():
    board = create_empty_board()

    set_positions(
        board,
        PLAYER_BLACK,
        [0, 1]
    )

    assert_test(
        not NineMensMorrisRules.is_mill(
            board,
            1,
            PLAYER_BLACK
        ),
        "Two pieces should not form a mill"
    )


def test_mixed_players_do_not_form_mill():
    board = create_empty_board()

    board.set_position(0, PLAYER_BLACK)
    board.set_position(1, PLAYER_BLACK)
    board.set_position(2, PLAYER_WHITE)

    assert_test(
        not NineMensMorrisRules.is_mill(
            board,
            1,
            PLAYER_BLACK
        ),
        "Mixed players should not form a mill"
    )


def test_get_mill_cells():
    board = create_empty_board()

    set_positions(
        board,
        PLAYER_BLACK,
        [0, 1, 2]
    )

    mills = NineMensMorrisRules.get_mill_cells(
        board,
        PLAYER_BLACK
    )

    assert_test(
        (0, 1, 2) in mills,
        "Mill 0-1-2 should be detected"
    )


# ============================================================
# FLYING
# ============================================================

def test_flying_with_three_pieces():
    board = create_empty_board()

    set_positions(
        board,
        PLAYER_BLACK,
        [0, 1, 2]
    )

    assert_test(
        NineMensMorrisRules.can_fly(
            board,
            PLAYER_BLACK
        ),
        "Player with exactly 3 pieces should be able to fly"
    )


def test_no_flying_with_more_than_three_pieces():
    board = create_empty_board()

    set_positions(
        board,
        PLAYER_BLACK,
        [0, 1, 2, 3]
    )

    assert_test(
        not NineMensMorrisRules.can_fly(
            board,
            PLAYER_BLACK
        ),
        "Player with more than 3 pieces should not fly"
    )


# ============================================================
# LEGAL DESTINATIONS
# ============================================================

def test_legal_adjacent_destination():
    board = create_empty_board()

    board.place_piece(
        0,
        PLAYER_BLACK
    )

    destinations = NineMensMorrisRules.get_legal_destinations(
        board,
        0,
        PLAYER_BLACK
    )

    assert_test(
        1 in destinations,
        "1 should be a legal destination from 0"
    )

    assert_test(
        9 in destinations,
        "9 should be a legal destination from 0"
    )


def test_non_adjacent_destination_not_allowed():
    board = create_empty_board()

    board.place_piece(
        0,
        PLAYER_BLACK
    )

    destinations = NineMensMorrisRules.get_legal_destinations(
        board,
        0,
        PLAYER_BLACK
    )

    assert_test(
        2 not in destinations,
        "2 should not be a legal destination from 0"
    )


def test_flying_allows_any_empty_position():
    board = create_empty_board()

    set_positions(
        board,
        PLAYER_BLACK,
        [0, 1, 2]
    )

    destinations = NineMensMorrisRules.get_legal_destinations(
        board,
        0,
        PLAYER_BLACK
    )

    assert_test(
        23 in destinations,
        "With 3 pieces, player should be able to fly to 23"
    )


# ============================================================
# LEGAL MOVES
# ============================================================

def test_get_legal_moves():
    board = create_empty_board()

    board.place_piece(
        0,
        PLAYER_BLACK
    )

    moves = NineMensMorrisRules.get_legal_moves(
        board,
        PLAYER_BLACK
    )

    assert_test(
        (0, 1) in moves,
        "Move 0 -> 1 should be legal"
    )

    assert_test(
        (0, 9) in moves,
        "Move 0 -> 9 should be legal"
    )


def test_has_legal_move():
    board = create_empty_board()

    board.place_piece(
        0,
        PLAYER_BLACK
    )

    assert_test(
        NineMensMorrisRules.has_legal_move(
            board,
            PLAYER_BLACK
        ),
        "Black should have a legal move"
    )


# ============================================================
# CAPTURE TESTS
# ============================================================

def test_can_remove_opponent_piece():
    board = create_empty_board()

    board.set_position(
        0,
        PLAYER_WHITE
    )

    assert_test(
        NineMensMorrisRules.can_remove_piece(
            board,
            0,
            PLAYER_BLACK
        ),
        "Black should be able to remove white piece"
    )


def test_cannot_remove_own_piece():
    board = create_empty_board()

    board.set_position(
        0,
        PLAYER_BLACK
    )

    assert_test(
        not NineMensMorrisRules.can_remove_piece(
            board,
            0,
            PLAYER_BLACK
        ),
        "Player should not remove own piece"
    )


def test_cannot_remove_empty_position():
    board = create_empty_board()

    assert_test(
        not NineMensMorrisRules.can_remove_piece(
            board,
            0,
            PLAYER_BLACK
        ),
        "Empty position cannot be removed"
    )


def test_mill_capture_restriction():
    board = create_empty_board()

    # White mill.
    set_positions(
        board,
        PLAYER_WHITE,
        [0, 1, 2]
    )

    # White also has a non-mill piece.
    board.set_position(
        3,
        PLAYER_WHITE
    )

    assert_test(
        not NineMensMorrisRules.can_remove_piece(
            board,
            0,
            PLAYER_BLACK
        ),
        "Mill piece should not be removable while non-mill piece exists"
    )

    assert_test(
        NineMensMorrisRules.can_remove_piece(
            board,
            3,
            PLAYER_BLACK
        ),
        "Non-mill piece should be removable"
    )


def test_get_removable_pieces():
    board = create_empty_board()

    set_positions(
        board,
        PLAYER_WHITE,
        [0, 1, 2]
    )

    board.set_position(
        3,
        PLAYER_WHITE
    )

    removable = NineMensMorrisRules.get_removable_pieces(
        board,
        PLAYER_BLACK
    )

    assert_test(
        removable == [3],
        "Only non-mill white piece should be removable"
    )


# ============================================================
# WIN CONDITIONS
# ============================================================

def test_player_wins_when_opponent_has_less_than_three():
    board = create_empty_board()

    set_positions(
        board,
        PLAYER_BLACK,
        [0, 1, 2]
    )

    set_positions(
        board,
        PLAYER_WHITE,
        [3, 4]
    )

    assert_test(
        NineMensMorrisRules.is_winner(
            board,
            PLAYER_BLACK
        ),
        "Black should win when White has fewer than 3 pieces"
    )


def test_three_opponent_pieces_do_not_trigger_piece_count_win():
    board = create_empty_board()

    set_positions(
        board,
        PLAYER_BLACK,
        [0, 1, 2]
    )

    set_positions(
        board,
        PLAYER_WHITE,
        [3, 4, 5]
    )

    assert_test(
        not NineMensMorrisRules.is_winner(
            board,
            PLAYER_BLACK
        ),
        "Three opponent pieces should not automatically mean loss"
    )


# ============================================================
# GAME PHASE
# ============================================================

def test_placement_phase():
    board = create_empty_board()

    phase = NineMensMorrisRules.get_phase(
        board,
        0
    )

    assert_test(
        phase == PHASE_PLACEMENT,
        "Game should start in placement phase"
    )


def test_placement_phase_before_all_pieces_are_placed():
    board = create_empty_board()

    phase = NineMensMorrisRules.get_phase(
        board,
        PIECES_PER_PLAYER * 2 - 1
    )

    assert_test(
        phase == PHASE_PLACEMENT,
        "Game should remain in placement phase"
    )


def test_movement_phase():
    board = create_empty_board()

    phase = NineMensMorrisRules.get_phase(
        board,
        PIECES_PER_PLAYER * 2
    )

    assert_test(
        phase == PHASE_MOVEMENT,
        "Game should enter movement phase after placement"
    )


# ============================================================
# OPPONENT TEST
# ============================================================

def test_get_opponent():
    assert_test(
        NineMensMorrisRules.get_opponent(
            PLAYER_BLACK
        ) == PLAYER_WHITE,
        "Black opponent should be White"
    )

    assert_test(
        NineMensMorrisRules.get_opponent(
            PLAYER_WHITE
        ) == PLAYER_BLACK,
        "White opponent should be Black"
    )

    assert_test(
        NineMensMorrisRules.get_opponent(
            EMPTY
        ) == EMPTY,
        "Empty should have no opponent"
    )


# ============================================================
# TEST RUNNER
# ============================================================

def run_all_tests():

    tests = [

        # Board
        test_board_initialization,
        test_valid_positions,
        test_invalid_positions,

        # Placement
        test_place_black_piece,
        test_place_white_piece,
        test_cannot_place_on_occupied_position,
        test_invalid_player_cannot_place,

        # Removal
        test_remove_piece,
        test_remove_empty_position,

        # Movement
        test_move_piece,
        test_move_wrong_player_piece,
        test_move_to_occupied_position,

        # Board information
        test_available_positions,
        test_player_positions,
        test_piece_count,
        test_empty_count,
        test_board_full,

        # Copy
        test_board_copy,

        # Adjacency
        test_position_adjacency,
        test_non_adjacent_positions,
        test_get_adjacent_positions,

        # Mills
        test_horizontal_mill,
        test_vertical_mill,
        test_incomplete_mill,
        test_mixed_players_do_not_form_mill,
        test_get_mill_cells,

        # Flying
        test_flying_with_three_pieces,
        test_no_flying_with_more_than_three_pieces,

        # Legal destinations
        test_legal_adjacent_destination,
        test_non_adjacent_destination_not_allowed,
        test_flying_allows_any_empty_position,

        # Legal moves
        test_get_legal_moves,
        test_has_legal_move,

        # Captures
        test_can_remove_opponent_piece,
        test_cannot_remove_own_piece,
        test_cannot_remove_empty_position,
        test_mill_capture_restriction,
        test_get_removable_pieces,

        # Win conditions
        test_player_wins_when_opponent_has_less_than_three,
        test_three_opponent_pieces_do_not_trigger_piece_count_win,

        # Game phases
        test_placement_phase,
        test_placement_phase_before_all_pieces_are_placed,
        test_movement_phase,

        # Opponent
        test_get_opponent,
    ]

    passed = 0
    failed = 0

    print("=" * 70)
    print("NINE MEN'S MORRIS TEST SUITE")
    print("=" * 70)

    for test in tests:

        try:
            test()

            print(
                f"[PASS] {test.__name__}"
            )

            passed += 1

        except Exception as error:

            print(
                f"[FAIL] {test.__name__}"
            )

            print(
                f"       {error}"
            )

            failed += 1

    print("=" * 70)
    print(f"Total Tests  : {len(tests)}")
    print(f"Tests Passed : {passed}")
    print(f"Tests Failed : {failed}")
    print("=" * 70)

    if failed == 0:
        print()
        print("ALL NINE MEN'S MORRIS TESTS PASSED.")
        print()

    else:
        print()
        print("SOME NINE MEN'S MORRIS TESTS FAILED.")
        print()


if __name__ == "__main__":
    run_all_tests()