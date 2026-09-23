# games/gomoku/ai.py
from __future__ import annotations
import random
from typing import Any
from engine.ai_base import AIBase
from engine.utils.constants import Difficulty
from games.gomoku.constants import (BOARD_COLUMNS,BOARD_ROWS,EMPTY,PLAYER_BLACK,PLAYER_WHITE,)
class GomokuAI(AIBase):
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
        candidates = self._get_adjacent_empty_cells(board, distance=1)
        if candidates and random.random() < 0.4:
            return random.choice(candidates)
        return random.choice(legal_moves)
    def _select_hard_move(self,game_state: dict[str, Any],legal_moves: list[tuple[int, int]],) -> tuple[int, int] | None:
        board = game_state.get("board")
        if not board:
            return random.choice(legal_moves)
        if len(legal_moves) == BOARD_ROWS * BOARD_COLUMNS:
            return (BOARD_ROWS // 2, BOARD_COLUMNS // 2)
        candidates = self._get_adjacent_empty_cells(board, distance=1)
        if not candidates:
            candidates = legal_moves
        win_move = self._find_winning_move(board, candidates, self.player)
        if win_move:
            return win_move
        block_move = self._find_winning_move(board, candidates, self.opponent)
        if block_move:
            return block_move
        best_score = -float("inf")
        best_move = candidates[0]
        for r, c in candidates:
            score = self._score_cell_tactics(board, r, c)
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
        candidates = self._get_adjacent_empty_cells(board, distance=2)
        if not candidates:
            candidates = legal_moves
        win_move = self._find_winning_move(board, candidates, self.player)
        if win_move:
            return win_move
        block_move = self._find_winning_move(board, candidates, self.opponent)
        if block_move:
            return block_move
        ranked_candidates = sorted(candidates,key=lambda cell: self._score_cell_tactics(board, cell[0], cell[1]),reverse=True,)[:10]
        best_score = -float("inf")
        best_move = ranked_candidates[0]
        for r, c in ranked_candidates:
            board[r][c] = self.player
            score = self._alphabeta(board, depth=3, is_maximizing=False, alpha=-float("inf"), beta=float("inf"))
            board[r][c] = EMPTY
            if score > best_score:
                best_score = score
                best_move = (r, c)
        return best_move
    def _alphabeta(self,board: list[list[int]],depth: int,is_maximizing: bool,alpha: float,beta: float,) -> float:
        if depth == 0:
            return self._evaluate_board_patterns(board)
        candidates = self._get_adjacent_empty_cells(board, distance=1)
        if not candidates:
            return 0.0
        ranked = sorted(candidates,key=lambda cell: self._score_cell_tactics(board, cell[0], cell[1]),reverse=True,)[:6]
        if is_maximizing:
            max_eval = -float("inf")
            for r, c in ranked:
                board[r][c] = self.player
                eval_score = self._alphabeta(board, depth - 1, False, alpha, beta)
                board[r][c] = EMPTY
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float("inf")
            for r, c in ranked:
                board[r][c] = self.opponent
                eval_score = self._alphabeta(board, depth - 1, True, alpha, beta)
                board[r][c] = EMPTY
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval
    def _score_cell_tactics(self, board: list[list[int]], r: int, c: int) -> float:
        attack_score = self._count_lines_from_cell(board, r, c, self.player)
        defense_score = self._count_lines_from_cell(board, r, c, self.opponent) * 1.15
        center_r, center_c = BOARD_ROWS // 2, BOARD_COLUMNS // 2
        center_bonus = 15.0 - (abs(r - center_r) + abs(c - center_c))
        return attack_score + defense_score + max(0.0, center_bonus)
    def _count_lines_from_cell(self,board: list[list[int]],r: int,c: int,player: int,) -> float:
        directions = ((0, 1), (1, 0), (1, 1), (1, -1))
        total_score = 0.0
        for dr, dc in directions:
            count = 1
            nr, nc = r + dr, c + dc
            while 0 <= nr < BOARD_ROWS and 0 <= nc < BOARD_COLUMNS and board[nr][nc] == player:
                count += 1
                nr += dr
                nc += dc
            open_forward = (0 <= nr < BOARD_ROWS and 0 <= nc < BOARD_COLUMNS and board[nr][nc] == EMPTY)
            nr, nc = r - dr, c - dc
            while 0 <= nr < BOARD_ROWS and 0 <= nc < BOARD_COLUMNS and board[nr][nc] == player:
                count += 1
                nr -= dr
                nc -= dc
            open_backward = (0 <= nr < BOARD_ROWS and 0 <= nc < BOARD_COLUMNS and board[nr][nc] == EMPTY)
            open_ends = (1 if open_forward else 0) + (1 if open_backward else 0)
            if count >= 5:
                total_score += 100000.0
            elif count == 4:
                total_score += 25000.0 if open_ends == 2 else 5000.0
            elif count == 3:
                total_score += 3000.0 if open_ends == 2 else 300.0
            elif count == 2:
                total_score += 100.0 if open_ends == 2 else 10.0
        return total_score
    def _evaluate_board_patterns(self, board: list[list[int]]) -> float:
        p_score = 0.0
        o_score = 0.0
        occupied = [(r, c) for r in range(BOARD_ROWS) for c in range(BOARD_COLUMNS) if board[r][c] != EMPTY]
        for r, c in occupied:
            val = self._count_lines_from_cell(board, r, c, board[r][c])
            if board[r][c] == self.player:
                p_score += val
            else:
                o_score += val
        return p_score - o_score
    def _find_winning_move(self,board: list[list[int]],candidates: list[tuple[int, int]],player: int,) -> tuple[int, int] | None:
        for r, c in candidates:
            if self._count_lines_from_cell(board, r, c, player) >= 100000.0:
                return (r, c)
        return None
    @staticmethod
    def _get_adjacent_empty_cells(board: list[list[int]],distance: int = 1,) -> list[tuple[int, int]]:
        adjacent: set[tuple[int, int]] = set()
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLUMNS):
                if board[r][c] != EMPTY:
                    for dr in range(-distance, distance + 1):
                        for dc in range(-distance, distance + 1):
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < BOARD_ROWS and 0 <= nc < BOARD_COLUMNS:
                                if board[nr][nc] == EMPTY:
                                    adjacent.add((nr, nc))
        return list(adjacent)