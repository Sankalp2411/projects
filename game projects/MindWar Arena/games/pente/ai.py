# games/pente/ai.py
from __future__ import annotations
import random
from typing import Any
from engine.ai_base import AIBase
from engine.utils.constants import Difficulty
from games.pente.constants import (BOARD_COLUMNS,BOARD_ROWS,EMPTY,PLAYER_BLACK,PLAYER_WHITE,)
class PenteAI(AIBase):
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
        board = game_state.get("board")
        if not board:
            return random.choice(legal_moves)
        candidates = self._get_adjacent_empty(board, distance=1)
        if candidates and random.random() < 0.45:
            return random.choice(candidates)
        return random.choice(legal_moves)
    def _select_hard_move(self,game_state: dict[str, Any],legal_moves: list[tuple[int, int]],) -> tuple[int, int] | None:
        board = game_state.get("board")
        if not board:
            return random.choice(legal_moves)
        if len(legal_moves) == BOARD_ROWS * BOARD_COLUMNS:
            return (BOARD_ROWS // 2, BOARD_COLUMNS // 2)
        candidates = self._get_adjacent_empty(board, distance=1)
        if not candidates:
            candidates = legal_moves
        for r, c in candidates:
            if self._is_winning_placement(board, r, c, self.player, game_state):
                return (r, c)
        for r, c in candidates:
            if self._is_winning_placement(board, r, c, self.opponent, game_state):
                return (r, c)
        for r, c in candidates:
            if self._creates_capture(board, r, c, self.player):
                return (r, c)
        best_score = -float("inf")
        best_move = candidates[0]
        for r, c in candidates:
            score = self._score_tactics(board, r, c)
            if score > best_score:
                best_score = score
                best_move = (r, c)
        return best_move
    def _select_impossible_move(self,game_state: dict[str, Any],legal_moves: list[tuple[int, int]],) -> tuple[int, int] | None:
        board = game_state.get("board")
        if not board:
            return random.choice(legal_moves)
        if len(legal_moves) == BOARD_ROWS * BOARD_COLUMNS:
            return (BOARD_ROWS // 2, BOARD_COLUMNS // 2)
        candidates = self._get_adjacent_empty(board, distance=2)
        if not candidates:
            candidates = legal_moves
        for r, c in candidates:
            if self._is_winning_placement(board, r, c, self.player, game_state):
                return (r, c)
        for r, c in candidates:
            if self._is_winning_placement(board, r, c, self.opponent, game_state):
                return (r, c)
        for r, c in candidates:
            if self._creates_capture(board, r, c, self.opponent):
                return (r, c)
        ranked = sorted(candidates,key=lambda cell: self._score_tactics(board, cell[0], cell[1]),reverse=True,)[:8]
        best_score = -float("inf")
        best_move = ranked[0]
        for r, c in ranked:
            board[r][c] = self.player
            score = self._minimax_search(board, depth=2, is_maximizing=False, alpha=-float("inf"), beta=float("inf"))
            board[r][c] = EMPTY
            if score > best_score:
                best_score = score
                best_move = (r, c)
        return best_move
    def _minimax_search(self,board: list[list[int]],depth: int,is_maximizing: bool,alpha: float,beta: float,) -> float:
        if depth == 0:
            return self._evaluate_board(board)
        candidates = self._get_adjacent_empty(board, distance=1)
        if not candidates:
            return 0.0
        ranked = sorted(candidates,key=lambda cell: self._score_tactics(board, cell[0], cell[1]),reverse=True,)[:5]
        if is_maximizing:
            max_eval = -float("inf")
            for r, c in ranked:
                board[r][c] = self.player
                val = self._minimax_search(board, depth - 1, False, alpha, beta)
                board[r][c] = EMPTY
                max_eval = max(max_eval, val)
                alpha = max(alpha, val)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float("inf")
            for r, c in ranked:
                board[r][c] = self.opponent
                val = self._minimax_search(board, depth - 1, True, alpha, beta)
                board[r][c] = EMPTY
                min_eval = min(min_eval, val)
                beta = min(beta, val)
                if beta <= alpha:
                    break
            return min_eval
    def _score_tactics(self, board: list[list[int]], r: int, c: int) -> float:
        score = 0.0
        if self._creates_capture(board, r, c, self.player):
            score += 400.0
        if self._creates_capture(board, r, c, self.opponent):
            score += 300.0
        cr, cc = BOARD_ROWS // 2, BOARD_COLUMNS // 2
        score += max(0.0, 18.0 - (abs(r - cr) + abs(c - cc)))
        score += self._line_score(board, r, c, self.player)
        score += self._line_score(board, r, c, self.opponent) * 1.1
        return score
    def _line_score(self, board: list[list[int]], r: int, c: int, player: int) -> float:
        directions = ((0, 1), (1, 0), (1, 1), (1, -1))
        score = 0.0
        for dr, dc in directions:
            count = 1
            nr, nc = r + dr, c + dc
            while 0 <= nr < BOARD_ROWS and 0 <= nc < BOARD_COLUMNS and board[nr][nc] == player:
                count += 1
                nr += dr
                nc += dc
            nr, nc = r - dr, c - dc
            while 0 <= nr < BOARD_ROWS and 0 <= nc < BOARD_COLUMNS and board[nr][nc] == player:
                count += 1
                nr -= dr
                nc -= dc
            if count >= 5:
                score += 50000.0
            elif count == 4:
                score += 5000.0
            elif count == 3:
                score += 200.0
            elif count == 2:
                score += 20.0
        return score
    def _evaluate_board(self, board: list[list[int]]) -> float:
        score = 0.0
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLUMNS):
                piece = board[r][c]
                if piece == self.player:
                    score += self._line_score(board, r, c, self.player)
                elif piece == self.opponent:
                    score -= self._line_score(board, r, c, self.opponent)
        return score
    def _is_winning_placement(self,board: list[list[int]],r: int,c: int,player: int,game_state: dict[str, Any],) -> bool:
        if self._line_score(board, r, c, player) >= 50000.0:
            return True
        captures = game_state.get("capture_counts", {}).get(player, 0)
        if captures >= 4 and self._creates_capture(board, r, c, player):
            return True
        return False
    def _creates_capture(self, board: list[list[int]], r: int, c: int, player: int) -> bool:
        opponent = self.opponent if player == self.player else self.player
        directions = ((0, 1), (1, 0), (1, 1), (1, -1), (0, -1), (-1, 0), (-1, -1), (-1, 1))
        for dr, dc in directions:
            r1, c1 = r + dr, c + dc
            r2, c2 = r + dr * 2, c + dc * 2
            r3, c3 = r + dr * 3, c + dc * 3
            if 0 <= r3 < BOARD_ROWS and 0 <= c3 < BOARD_COLUMNS:
                if (board[r1][c1] == opponent and board[r2][c2] == opponent and board[r3][c3] == player):
                    return True
        return False
    @staticmethod
    def _get_adjacent_empty(board: list[list[int]],distance: int = 1,) -> list[tuple[int, int]]:
        adj: set[tuple[int, int]] = set()
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLUMNS):
                if board[r][c] != EMPTY:
                    for dr in range(-distance, distance + 1):
                        for dc in range(-distance, distance + 1):
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < BOARD_ROWS and 0 <= nc < BOARD_COLUMNS:
                                if board[nr][nc] == EMPTY:
                                    adj.add((nr, nc))
        return list(adj)