# games/chess/ai.py
from __future__ import annotations
import random
from typing import Any
from engine.ai_base import AIBase
from engine.utils.constants import Difficulty
from games.chess.board import ChessBoard
from games.chess.constants import (BLACK_BISHOP,BLACK_KING,BLACK_KNIGHT,BLACK_PAWN,BLACK_QUEEN,BLACK_ROOK,EMPTY,KING_VALUE,PLAYER_BLACK,PLAYER_WHITE,WHITE_BISHOP,WHITE_KING,WHITE_KNIGHT,WHITE_PAWN,WHITE_QUEEN,WHITE_ROOK,)
from games.chess.rules import ChessRules
PIECE_VALUES = {WHITE_PAWN: 100,WHITE_KNIGHT: 320,WHITE_BISHOP: 330,WHITE_ROOK: 500,WHITE_QUEEN: 900,WHITE_KING: 20000,BLACK_PAWN: -100,BLACK_KNIGHT: -320,BLACK_BISHOP: -330,BLACK_ROOK: -500,BLACK_QUEEN: -900,BLACK_KING: -20000,EMPTY: 0,}
PST_PAWN = ((0, 0, 0, 0, 0, 0, 0, 0),(50, 50, 50, 50, 50, 50, 50, 50),(10, 10, 20, 30, 30, 20, 10, 10),(5, 5, 10, 25, 25, 10, 5, 5),(0, 0, 0, 20, 20, 0, 0, 0),(5, -5, -10, 0, 0, -10, -5, 5),(5, 10, 10, -20, -20, 10, 10, 5),(0, 0, 0, 0, 0, 0, 0, 0),)
PST_KNIGHT = ((-50, -40, -30, -30, -30, -30, -40, -50),(-40, -20, 0, 0, 0, 0, -20, -40),(-30, 0, 10, 15, 15, 10, 0, -30),(-30, 5, 15, 20, 20, 15, 5, -30),(-30, 0, 15, 20, 20, 15, 0, -30),(-30, 5, 10, 15, 15, 10, 5, -30),(-40, -20, 0, 5, 5, 0, -20, -40),(-50, -40, -30, -30, -30, -30, -40, -50),)
PST_BISHOP = ((-20, -10, -10, -10, -10, -10, -10, -20),(-10, 0, 0, 0, 0, 0, 0, -10),(-10, 0, 5, 10, 10, 5, 0, -10),(-10, 5, 5, 10, 10, 5, 5, -10),(-10, 0, 10, 10, 10, 10, 0, -10),(-10, 10, 10, 10, 10, 10, 10, -10),(-10, 5, 0, 0, 0, 0, 5, -10),(-20, -10, -10, -10, -10, -10, -10, -20),)
PST_KING = ((-30, -40, -40, -50, -50, -40, -40, -30),(-30, -40, -40, -50, -50, -40, -40, -30),(-30, -40, -40, -50, -50, -40, -40, -30),(-30, -40, -40, -50, -50, -40, -40, -30),(-20, -30, -30, -40, -40, -30, -30, -20),(-10, -20, -20, -20, -20, -20, -20, -10),(20, 20, 0, 0, 0, 0, 20, 20),(20, 30, 10, 0, 0, 10, 30, 20),)
class ChessAI(AIBase):
    def __init__(self,player: int = PLAYER_BLACK,difficulty: Difficulty = Difficulty.MEDIUM,) -> None:
        super().__init__(player=player, difficulty=difficulty)
        self.opponent = PLAYER_WHITE if player == PLAYER_BLACK else PLAYER_BLACK
        self.search_depth = 2
        self.initialized = True
    def initialize(self) -> None:
        self.initialized = True
    def reset(self) -> None:
        super().reset()
        self.initialized = True
    def set_player(self, player: int) -> None:
        super().set_player(player)
        self.opponent = PLAYER_WHITE if player == PLAYER_BLACK else PLAYER_BLACK
    def _select_beginner_move(self,game_state: dict[str, Any],legal_moves: list[tuple[int, ...]],) -> tuple[int, ...] | None:
        valid = [m for m in legal_moves if self._is_valid_move_format(m)]
        if not valid:
            return None
        return random.choice(valid)
    def _select_hard_move(self,game_state: dict[str, Any],legal_moves: list[tuple[int, ...]],) -> tuple[int, ...] | None:
        return self._search_best_move(game_state, legal_moves, depth=3)
    def _select_impossible_move(self,game_state: dict[str, Any],legal_moves: list[tuple[int, ...]],) -> tuple[int, ...] | None:
        return self._search_best_move(game_state, legal_moves, depth=4)
    def _search_best_move(self,game_state: dict[str, Any],legal_moves: list[tuple[int, ...]],depth: int,) -> tuple[int, ...] | None:
        board_state = game_state.get("board")
        if not board_state:
            valid = [m for m in legal_moves if self._is_valid_move_format(m)]
            return random.choice(valid) if valid else None
        board = self._create_board(board_state)
        en_passant = game_state.get("en_passant_target")
        castling = game_state.get("castling_rights")
        valid_moves = [m for m in legal_moves if self._is_valid_move_format(m)]
        if not valid_moves:
            return None
        def move_priority(m: tuple[int, ...]) -> int:
            tr, tc = m[2], m[3]
            target = board.get_cell(tr, tc)
            return abs(PIECE_VALUES.get(target, 0))
        ordered_moves = sorted(valid_moves, key=move_priority, reverse=True)
        best_move = ordered_moves[0]
        if self.player == PLAYER_WHITE:
            best_score = -float("inf")
            alpha = -float("inf")
            beta = float("inf")
            for move in ordered_moves:
                sim_board = self.simulate_move(board, move, self.player, en_passant, castling)
                if sim_board is None:
                    continue
                score = self._alphabeta(sim_board, depth - 1, PLAYER_BLACK, alpha, beta, None, castling)
                if score > best_score:
                    best_score = score
                    best_move = move
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
        else:
            best_score = float("inf")
            alpha = -float("inf")
            beta = float("inf")
            for move in ordered_moves:
                sim_board = self.simulate_move(board, move, self.player, en_passant, castling)
                if sim_board is None:
                    continue
                score = self._alphabeta(sim_board, depth - 1, PLAYER_WHITE, alpha, beta, None, castling)
                if score < best_score:
                    best_score = score
                    best_move = move
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
        return tuple(best_move)
    def _alphabeta(self,board: ChessBoard,depth: int,player: int,alpha: float,beta: float,en_passant_target: tuple[int, int] | None,castling_rights: dict[str, bool] | None,) -> float:
        if depth <= 0:
            return self._evaluate_board(board)
        legal_moves = ChessRules.get_legal_moves(board, player, en_passant_target, castling_rights)
        if not legal_moves:
            if ChessRules.is_in_check(board, player):
                return -(KING_VALUE + depth) if player == PLAYER_WHITE else (KING_VALUE + depth)
            return 0.0
        next_player = PLAYER_BLACK if player == PLAYER_WHITE else PLAYER_WHITE
        if player == PLAYER_WHITE:
            value = -float("inf")
            for move in legal_moves:
                sim_board = self.simulate_move(board, move, player, en_passant_target, castling_rights)
                if sim_board is None:
                    continue
                score = self._alphabeta(sim_board, depth - 1, next_player, alpha, beta, None, castling_rights)
                value = max(value, score)
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
            return value
        else:
            value = float("inf")
            for move in legal_moves:
                sim_board = self.simulate_move(
                    board, move, player, en_passant_target, castling_rights
                )
                if sim_board is None:
                    continue
                score = self._alphabeta(
                    sim_board, depth - 1, next_player, alpha, beta, None, castling_rights
                )
                value = min(value, score)
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value
    def _evaluate_board(self, board: ChessBoard) -> float:
        total = 0.0
        for r in range(8):
            for c in range(8):
                piece = board.get_cell(r, c)
                if piece == EMPTY:
                    continue
                val = PIECE_VALUES.get(piece, 0)
                pst_val = 0
                if piece == WHITE_PAWN:
                    pst_val = PST_PAWN[r][c]
                elif piece == BLACK_PAWN:
                    pst_val = -PST_PAWN[7 - r][c]
                elif piece == WHITE_KNIGHT:
                    pst_val = PST_KNIGHT[r][c]
                elif piece == BLACK_KNIGHT:
                    pst_val = -PST_KNIGHT[7 - r][c]
                elif piece == WHITE_BISHOP:
                    pst_val = PST_BISHOP[r][c]
                elif piece == BLACK_BISHOP:
                    pst_val = -PST_BISHOP[7 - r][c]
                elif piece == WHITE_KING:
                    pst_val = PST_KING[r][c]
                elif piece == BLACK_KING:
                    pst_val = -PST_KING[7 - r][c]
                total += val + pst_val
        return total
    @staticmethod
    def simulate_move(board: ChessBoard,move: tuple[int, ...],player: int,en_passant_target: tuple[int, int] | None = None,castling_rights: dict[str, bool] | None = None,) -> ChessBoard | None:
        if board is None:
            return None
        simulated_board = board.copy()
        if not ChessRules.apply_legal_move(simulated_board, move, player, en_passant_target, castling_rights):
            return None
        return simulated_board
    @staticmethod
    def _is_valid_move_format(move: Any) -> bool:
        if not isinstance(move, (tuple, list)):
            return False
        if len(move) not in (4, 5):
            return False
        return all(isinstance(v, int) for v in move[:4])
    @staticmethod
    def _create_board(board_state: list[list[int]]) -> ChessBoard:
        board = ChessBoard()
        board._board = [list(row) for row in board_state]
        return board