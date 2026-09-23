# games/checkers/ai.py
from __future__ import annotations
import random
from typing import Any
from engine.ai_base import AIBase
from engine.utils.constants import Difficulty
from games.checkers.board import CheckersBoard
from games.checkers.constants import (BLACK_KING,BLACK_MAN,EMPTY,PLAYER_BLACK,PLAYER_WHITE,WHITE_KING,WHITE_MAN,)
from games.checkers.rules import CheckersRules
class CheckersAI(AIBase):
    def __init__(self,player: int = PLAYER_WHITE,difficulty: Difficulty = Difficulty.MEDIUM,) -> None:
        super().__init__(player=player, difficulty=difficulty)
        self.opponent = PLAYER_BLACK if player == PLAYER_WHITE else PLAYER_WHITE
        self.initialized = True
    def initialize(self) -> None:
        self.initialized = True
    def reset(self) -> None:
        super().reset()
        self.initialized = True
    def set_player(self, player: int) -> None:
        super().set_player(player)
        self.opponent = PLAYER_BLACK if player == PLAYER_WHITE else PLAYER_WHITE
    def _select_beginner_move(self,game_state: dict[str, Any],legal_moves: list[tuple[int, int, int, int]],) -> tuple[int, int, int, int] | None:
        return random.choice(legal_moves)
    def _select_hard_move(self,game_state: dict[str, Any],legal_moves: list[tuple[int, int, int, int]],) -> tuple[int, int, int, int] | None:
        board_state = game_state.get("board")
        if not board_state:
            return random.choice(legal_moves)
        board = self._create_board(board_state)
        best_score = -float("inf")
        best_move = legal_moves[0]
        for move in legal_moves:
            sim_board = board.copy()
            CheckersRules.apply_move(sim_board, move, self.player)
            score = self._alphabeta(sim_board, depth=5, is_maximizing=False, alpha=-float("inf"), beta=float("inf"))
            if score > best_score:
                best_score = score
                best_move = move
        return best_move
    def _select_impossible_move(self,game_state: dict[str, Any],legal_moves: list[tuple[int, int, int, int]],) -> tuple[int, int, int, int] | None:
        board_state = game_state.get("board")
        if not board_state:
            return random.choice(legal_moves)
        board = self._create_board(board_state)
        best_score = -float("inf")
        best_move = legal_moves[0]
        alpha = -float("inf")
        beta = float("inf")
        for move in legal_moves:
            sim_board = board.copy()
            CheckersRules.apply_move(sim_board, move, self.player)
            score = self._alphabeta(sim_board, depth=7, is_maximizing=False, alpha=alpha, beta=beta)
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_move
    def _alphabeta(self,board: CheckersBoard,depth: int,is_maximizing: bool,alpha: float,beta: float,) -> float:
        current_player = self.player if is_maximizing else self.opponent
        legal_moves = CheckersRules.get_legal_moves(board, current_player)
        if not legal_moves or depth == 0:
            return self._evaluate_board(board)
        if is_maximizing:
            max_eval = -float("inf")
            for move in legal_moves:
                sim_board = board.copy()
                CheckersRules.apply_move(sim_board, move, self.player)
                eval_score = self._alphabeta(sim_board, depth - 1, False, alpha, beta)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float("inf")
            for move in legal_moves:
                sim_board = board.copy()
                CheckersRules.apply_move(sim_board, move, self.opponent)
                eval_score = self._alphabeta(sim_board, depth - 1, True, alpha, beta)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval
    def _evaluate_board(self, board: CheckersBoard) -> float:
        score = 0.0
        for r in range(8):
            for c in range(8):
                piece = board.get_cell(r, c)
                if piece == EMPTY:
                    continue
                val = 0.0
                if piece in (BLACK_MAN, WHITE_MAN):
                    val = 100.0
                    if piece == BLACK_MAN:
                        val += r * 6.0
                        if r == 0:
                            val += 15.0
                    else:
                        val += (7 - r) * 6.0
                        if r == 7:
                            val += 15.0
                    if 2 <= c <= 5:
                        val += 6.0
                elif piece in (BLACK_KING, WHITE_KING):
                    val = 260.0
                    if 2 <= r <= 5 and 2 <= c <= 5:
                        val += 10.0
                if CheckersRules.is_player_piece(piece, self.player):
                    score += val
                else:
                    score -= val
        return score
    @staticmethod
    def _create_board(board_state: list[list[int]]) -> CheckersBoard:
        board = CheckersBoard()
        board._board = [list(row) for row in board_state]
        return board