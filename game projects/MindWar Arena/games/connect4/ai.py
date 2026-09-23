# games/connect4/ai.py
from __future__ import annotations
import random
from typing import Any
from engine.ai_base import AIBase
from engine.utils.constants import Difficulty
from games.connect4.constants import (BOARD_COLUMNS,BOARD_ROWS,EMPTY,PLAYER_RED,PLAYER_YELLOW,)
class Connect4AI(AIBase):
    def __init__(self,player: int = PLAYER_YELLOW,difficulty: Difficulty = Difficulty.MEDIUM,) -> None:
        super().__init__(player=player, difficulty=difficulty)
        self.opponent = PLAYER_RED if player == PLAYER_YELLOW else PLAYER_YELLOW
        self.initialized = True
    def initialize(self) -> None:
        self.initialized = True
    def reset(self) -> None:
        super().reset()
        self.initialized = True
    def set_player(self, player: int) -> None:
        super().set_player(player)
        self.opponent = PLAYER_RED if player == PLAYER_YELLOW else PLAYER_YELLOW
    def _select_beginner_move(self,game_state: dict[str, Any],legal_moves: list[int],) -> int | None:
        board = game_state.get("board")
        if board and random.random() < 0.35:
            win_col = self._find_winning_move(board, legal_moves, self.player)
            if win_col is not None:
                return win_col
        return random.choice(legal_moves)
    def _select_hard_move(self,game_state: dict[str, Any],legal_moves: list[int],) -> int | None:
        board = game_state.get("board")
        if not board:
            return random.choice(legal_moves)
        win_col = self._find_winning_move(board, legal_moves, self.player)
        if win_col is not None:
            return win_col
        block_col = self._find_winning_move(board, legal_moves, self.opponent)
        if block_col is not None:
            return block_col
        return self._run_minimax(board, legal_moves, depth=4)
    def _select_impossible_move(self,game_state: dict[str, Any],legal_moves: list[int],) -> int | None:
        board = game_state.get("board")
        if not board:
            return random.choice(legal_moves)
        win_col = self._find_winning_move(board, legal_moves, self.player)
        if win_col is not None:
            return win_col
        block_col = self._find_winning_move(board, legal_moves, self.opponent)
        if block_col is not None:
            return block_col
        return self._run_minimax(board, legal_moves, depth=7)
    def _run_minimax(self,board: list[list[int]],legal_moves: list[int],depth: int,) -> int | None:
        center = BOARD_COLUMNS // 2
        ordered_moves = sorted(legal_moves, key=lambda c: abs(c - center))
        best_score = -float("inf")
        best_col = ordered_moves[0]
        alpha = -float("inf")
        beta = float("inf")
        for col in ordered_moves:
            row = self._get_drop_row(board, col)
            if row is None:
                continue
            board[row][col] = self.player
            score = self._alphabeta(board, depth - 1, alpha, beta, False)
            board[row][col] = EMPTY
            if score > best_score:
                best_score = score
                best_col = col
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_col
    def _alphabeta(self,board: list[list[int]],depth: int,alpha: float,beta: float,is_maximizing: bool,) -> float:
        if self._check_win_for_player(board, self.player):
            return 10000.0 + depth
        if self._check_win_for_player(board, self.opponent):
            return -10000.0 - depth
        valid_cols = [c for c in range(BOARD_COLUMNS) if board[0][c] == EMPTY]
        if not valid_cols or depth == 0:
            return self._score_position(board)
        center = BOARD_COLUMNS // 2
        ordered = sorted(valid_cols, key=lambda c: abs(c - center))
        if is_maximizing:
            value = -float("inf")
            for col in ordered:
                row = self._get_drop_row(board, col)
                if row is None:
                    continue
                board[row][col] = self.player
                value = max(value, self._alphabeta(board, depth - 1, alpha, beta, False))
                board[row][col] = EMPTY
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:
            value = float("inf")
            for col in ordered:
                row = self._get_drop_row(board, col)
                if row is None:
                    continue
                board[row][col] = self.opponent
                value = min(value, self._alphabeta(board, depth - 1, alpha, beta, True))
                board[row][col] = EMPTY
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value
    def _score_position(self, board: list[list[int]]) -> float:
        score = 0.0
        center_col = BOARD_COLUMNS // 2
        center_count = sum(1 for r in range(BOARD_ROWS) if board[r][center_col] == self.player)
        score += center_count * 3.0
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLUMNS - 3):
                window = [board[r][c + i] for i in range(4)]
                score += self._evaluate_window(window)
        for c in range(BOARD_COLUMNS):
            for r in range(BOARD_ROWS - 3):
                window = [board[r + i][c] for i in range(4)]
                score += self._evaluate_window(window)
        for r in range(BOARD_ROWS - 3):
            for c in range(BOARD_COLUMNS - 3):
                window = [board[r + i][c + i] for i in range(4)]
                score += self._evaluate_window(window)
        for r in range(3, BOARD_ROWS):
            for c in range(BOARD_COLUMNS - 3):
                window = [board[r - i][c + i] for i in range(4)]
                score += self._evaluate_window(window)
        return score
    def _evaluate_window(self, window: list[int]) -> float:
        score = 0.0
        p_count = window.count(self.player)
        o_count = window.count(self.opponent)
        empty_count = window.count(EMPTY)
        if p_count == 4:
            score += 1000.0
        elif p_count == 3 and empty_count == 1:
            score += 10.0
        elif p_count == 2 and empty_count == 2:
            score += 2.0
        if o_count == 3 and empty_count == 1:
            score -= 80.0
        elif o_count == 2 and empty_count == 2:
            score -= 5.0
        return score
    @staticmethod
    def _get_drop_row(board: list[list[int]], column: int) -> int | None:
        for r in range(BOARD_ROWS - 1, -1, -1):
            if board[r][column] == EMPTY:
                return r
        return None
    def _find_winning_move(self,board: list[list[int]],legal_moves: list[int],player: int,) -> int | None:
        for col in legal_moves:
            row = self._get_drop_row(board, col)
            if row is not None:
                board[row][col] = player
                won = self._check_win_for_player(board, player)
                board[row][col] = EMPTY
                if won:
                    return col
        return None
    @staticmethod
    def _check_win_for_player(board: list[list[int]], player: int) -> bool:
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLUMNS - 3):
                if all(board[r][c + i] == player for i in range(4)):
                    return True
        for c in range(BOARD_COLUMNS):
            for r in range(BOARD_ROWS - 3):
                if all(board[r + i][c] == player for i in range(4)):
                    return True
        for r in range(BOARD_ROWS - 3):
            for c in range(BOARD_COLUMNS - 3):
                if all(board[r + i][c + i] == player for i in range(4)):
                    return True
        for r in range(3, BOARD_ROWS):
            for c in range(BOARD_COLUMNS - 3):
                if all(board[r - i][c + i] == player for i in range(4)):
                    return True
        return False