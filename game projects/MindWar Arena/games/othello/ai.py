# games/othello/ai.py
from __future__ import annotations
import random
from typing import Any
from engine.ai_base import AIBase
from engine.utils.constants import Difficulty
from games.othello.board import OthelloBoard
from games.othello.constants import (BOARD_COLUMNS,BOARD_ROWS,PLAYER_BLACK,PLAYER_WHITE,)
from games.othello.rules import OthelloRules
POSITION_WEIGHTS = [[100, -20, 10, 5, 5, 10, -20, 100],[-20, -50, -2, -2, -2, -2, -50, -20],[10, -2, -1, -1, -1, -1, -2, 10],[5, -2, -1, 0, 0, -1, -2, 5],[5, -2, -1, 0, 0, -1, -2, 5],[10, -2, -1, -1, -1, -1, -2, 10],[-20, -50, -2, -2, -2, -2, -50, -20],[100, -20, 10, 5, 5, 10, -20, 100],]
class OthelloAI(AIBase):
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
    def _select_beginner_move(self,game_state: dict[str, Any],legal_moves: list[tuple[int, int]],) -> tuple[int, int] | None:
        return random.choice(legal_moves)
    def _select_hard_move(self,game_state: dict[str, Any],legal_moves: list[tuple[int, int]],) -> tuple[int, int] | None:
        board_state = game_state.get("board")
        if not board_state:
            return random.choice(legal_moves)
        corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
        for c in corners:
            if c in legal_moves:
                return c
        board = self._create_board(board_state)
        best_score = -float("inf")
        best_move = legal_moves[0]
        alpha = -float("inf")
        beta = float("inf")
        ordered_moves = sorted(legal_moves, key=lambda m: POSITION_WEIGHTS[m[0]][m[1]], reverse=True)
        for r, c in ordered_moves:
            sim_board = board.copy()
            OthelloRules.apply_move(sim_board, r, c, self.player)
            score = self._alphabeta(sim_board, depth=3, is_maximizing=False, alpha=alpha, beta=beta)
            if score > best_score:
                best_score = score
                best_move = (r, c)
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_move
    def _select_impossible_move(self,game_state: dict[str, Any],legal_moves: list[tuple[int, int]],) -> tuple[int, int] | None:
        board_state = game_state.get("board")
        if not board_state:
            return random.choice(legal_moves)
        corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
        for c in corners:
            if c in legal_moves:
                return c
        board = self._create_board(board_state)
        best_score = -float("inf")
        best_move = legal_moves[0]
        alpha = -float("inf")
        beta = float("inf")
        ordered_moves = sorted(legal_moves, key=lambda m: POSITION_WEIGHTS[m[0]][m[1]], reverse=True)
        for r, c in ordered_moves:
            sim_board = board.copy()
            OthelloRules.apply_move(sim_board, r, c, self.player)
            score = self._alphabeta(sim_board, depth=3, is_maximizing=False, alpha=alpha, beta=beta)
            if score > best_score:
                best_score = score
                best_move = (r, c)
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_move
    def _alphabeta(self,board: OthelloBoard,depth: int,is_maximizing: bool,alpha: float,beta: float,) -> float:
        if depth == 0 or OthelloRules.is_game_over(board):
            return self._evaluate_board(board)
        current_player = self.player if is_maximizing else self.opponent
        moves = OthelloRules.get_legal_moves(board, current_player)
        if not moves:
            other_player = self.opponent if is_maximizing else self.player
            other_moves = OthelloRules.get_legal_moves(board, other_player)
            if not other_moves:
                return self._evaluate_board(board)
            return self._alphabeta(board, depth - 1, not is_maximizing, alpha, beta)
        ordered_moves = sorted(moves, key=lambda m: POSITION_WEIGHTS[m[0]][m[1]], reverse=is_maximizing)[:8]
        if is_maximizing:
            max_eval = -float("inf")
            for r, c in ordered_moves:
                sim_board = board.copy()
                OthelloRules.apply_move(sim_board, r, c, self.player)
                eval_score = self._alphabeta(sim_board, depth - 1, False, alpha, beta)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float("inf")
            for r, c in ordered_moves:
                sim_board = board.copy()
                OthelloRules.apply_move(sim_board, r, c, self.opponent)
                eval_score = self._alphabeta(sim_board, depth - 1, True, alpha, beta)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval
    def _evaluate_board(self, board: OthelloBoard) -> float:
        score = 0.0
        p_count = 0
        o_count = 0
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLUMNS):
                val = board.get_cell(r, c)
                if val == self.player:
                    p_count += 1
                    score += POSITION_WEIGHTS[r][c]
                elif val == self.opponent:
                    o_count += 1
                    score -= POSITION_WEIGHTS[r][c]
        p_mobility = len(OthelloRules.get_legal_moves(board, self.player))
        o_mobility = len(OthelloRules.get_legal_moves(board, self.opponent))
        mobility_diff = p_mobility - o_mobility
        score += mobility_diff * 5.0
        if p_count + o_count > 50:
            score += (p_count - o_count) * 10.0
        return score
    @staticmethod
    def _create_board(board_state: list[list[int]]) -> OthelloBoard:
        board = OthelloBoard()
        board._board = [list(row) for row in board_state]
        return board