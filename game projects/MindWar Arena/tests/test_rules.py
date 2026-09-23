"""Unit tests for individual game rules and board mechanics."""

from games.checkers.board import CheckersBoard
from games.checkers.constants import PLAYER_BLACK, PLAYER_WHITE
from games.checkers.rules import CheckersRules
from games.chess.board import ChessBoard
from games.chess.rules import ChessRules
from games.connect4.board import Connect4Board
from games.connect4.constants import PLAYER_RED
from games.connect4.rules import Connect4Rules
from games.othello.board import OthelloBoard
from games.othello.rules import OthelloRules
from games.tic_tac_toe.board import TicTacToeBoard
from games.tic_tac_toe.constants import PLAYER_X
from games.tic_tac_toe.rules import TicTacToeRules


def test_tic_tac_toe_rules():
    board = TicTacToeBoard()
    # Initial board: all empty, 9 legal moves
    assert len(TicTacToeRules.get_legal_moves(board)) == 9

    # Winning row
    board.set_cell(0, 0, PLAYER_X)
    board.set_cell(0, 1, PLAYER_X)
    board.set_cell(0, 2, PLAYER_X)

    result = TicTacToeRules.evaluate_game(board)
    assert result.game_over is True
    assert result.winner == PLAYER_X
    assert result.draw is False


def test_connect4_rules():
    board = Connect4Board()
    # 7 columns available initially
    assert len(board.get_available_columns()) == 7

    # Drop 4 red tokens in column 0 for vertical win
    for _ in range(4):
        board.drop_piece(0, PLAYER_RED)

    result = Connect4Rules.evaluate_game(board)
    assert result.game_over is True
    assert result.winner == PLAYER_RED


def test_checkers_rules():
    board = CheckersBoard()
    # Checkers standard setup: 12 white pieces, 12 black pieces
    assert board.count_pieces(PLAYER_WHITE) == 12
    assert board.count_pieces(PLAYER_BLACK) == 12

    # Black moves first, should have legal moves
    moves = CheckersRules.get_legal_moves(board, PLAYER_BLACK)
    assert len(moves) > 0
    # Every initial move is non-capture (row distance 1)
    for r1, c1, r2, c2 in moves:
        assert abs(r2 - r1) == 1
        assert abs(c2 - c1) == 1


def test_othello_rules():
    board = OthelloBoard()
    # Standard Othello setup: 2 black discs, 2 white discs in center
    assert board.count_stones(1) == 2
    assert board.count_stones(2) == 2

    # Player 1 (Black) has 4 opening moves: (2,3), (3,2), (4,5), (5,4)
    moves = OthelloRules.get_legal_moves(board, 1)
    assert len(moves) == 4


def test_chess_rules():
    board = ChessBoard()
    # Standard chess setup: 16 pieces for White, 16 for Black
    state = board.get_board_state()
    white_pieces = [p for row in state for p in row if ChessBoard.is_white_piece(p)]
    black_pieces = [p for row in state for p in row if ChessBoard.is_black_piece(p)]
    assert len(white_pieces) == 16
    assert len(black_pieces) == 16

    # White opening legal moves: 16 pawn moves + 4 knight moves = 20 legal moves
    legal_moves = ChessRules.get_legal_moves(board, 1)
    assert len(legal_moves) == 20
