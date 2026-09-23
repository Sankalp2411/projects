# games/tic_tac_toe/ai.py
from __future__ import annotations
import random
from typing import Any
from engine.ai_base import AIBase
from engine.utils.constants import Difficulty
from games.tic_tac_toe.constants import (BOARD_COLUMNS,BOARD_ROWS,EMPTY,PLAYER_O,PLAYER_X,)
class TicTacToeAI(AIBase):
    def __init__(self,player: int = PLAYER_O,difficulty: Difficulty = Difficulty.MEDIUM,) -> None:
        super().__init__(player=player, difficulty=difficulty)
        self.opponent = PLAYER_X if player == PLAYER_O else PLAYER_O
        self.initialized = True
    def initialize(self) -> None:
        self.initialized = True
    def reset(self) -> None:
        super().reset()
        self.initialized = True
    def set_player(self, player: int) -> None:
        super().set_player(player)
        self.opponent = PLAYER_X if player == PLAYER_O else PLAYER_O
    def _select_beginner_move(self,game_state: dict[str, Any],legal_moves: list[tuple[int, int]],) -> tuple[int, int] | None:
        board = game_state.get("board")
        if board and random.random() < 0.3:
            win_move = self._find_immediate_win(board, legal_moves, self.player)
            if win_move:
                return win_move
        return random.choice(legal_moves)
    def _select_hard_move(self,game_state: dict[str, Any],legal_moves: list[tuple[int, int]],) -> tuple[int, int] | None:
        board = game_state.get("board")
        if not board:
            return random.choice(legal_moves)
        win_move = self._find_immediate_win(board, legal_moves, self.player)
        if win_move:
            return win_move
        block_move = self._find_immediate_win(board, legal_moves, self.opponent)
        if block_move:
            return block_move
        if (1, 1) in legal_moves and random.random() < 0.8:
            return (1, 1)
        return self._run_minimax(board, max_depth=3)
    def _select_impossible_move(self,game_state: dict[str, Any],legal_moves: list[tuple[int, int]],) -> tuple[int, int] | None:
        board = game_state.get("board")
        if not board:
            return random.choice(legal_moves)
        if len(legal_moves) == 9:
            return (1, 1)
        return self._run_minimax(board, max_depth=9)
    def _run_minimax(self,board: list[list[int]],max_depth: int,) -> tuple[int, int] | None:
        best_score = -float("inf")
        best_move = None
        legal_moves = self._get_empty_cells(board)
        for row, col in legal_moves:
            board[row][col] = self.player
            score = self._minimax(board,depth=0,max_depth=max_depth,is_maximizing=False,alpha=-float("inf"),beta=float("inf"),)
            board[row][col] = EMPTY
            if score > best_score:
                best_score = score
                best_move = (row, col)
        return best_move if best_move else (legal_moves[0] if legal_moves else None)
    def _minimax(self,board: list[list[int]],depth: int,max_depth: int,is_maximizing: bool,alpha: float,beta: float,) -> float:
        winner = self._check_fast_winner(board)
        if winner == self.player:
            return 10.0 - depth
        if winner == self.opponent:
            return depth - 10.0
        if not self._has_empty_cells(board) or depth >= max_depth:
            return 0.0
        if is_maximizing:
            max_eval = -float("inf")
            for r, c in self._get_empty_cells(board):
                board[r][c] = self.player
                eval_score = self._minimax(board, depth + 1, max_depth, False, alpha, beta)
                board[r][c] = EMPTY
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float("inf")
            for r, c in self._get_empty_cells(board):
                board[r][c] = self.opponent
                eval_score = self._minimax(board, depth + 1, max_depth, True, alpha, beta)
                board[r][c] = EMPTY
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval
    @staticmethod
    def _get_empty_cells(board: list[list[int]]) -> list[tuple[int, int]]:
        cells = []
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLUMNS):
                if board[r][c] == EMPTY:
                    cells.append((r, c))
        return cells
    @staticmethod
    def _has_empty_cells(board: list[list[int]]) -> bool:
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLUMNS):
                if board[r][c] == EMPTY:
                    return True
        return False
    @staticmethod
    def _check_fast_winner(board: list[list[int]]) -> int:
        for r in range(3):
            if board[r][0] != EMPTY and board[r][0] == board[r][1] == board[r][2]:
                return board[r][0]
        for c in range(3):
            if board[0][c] != EMPTY and board[0][c] == board[1][c] == board[2][c]:
                return board[0][c]
        if board[0][0] != EMPTY and board[0][0] == board[1][1] == board[2][2]:
            return board[0][0]
        if board[0][2] != EMPTY and board[0][2] == board[1][1] == board[2][0]:
            return board[0][2]
        return 0
    def _find_immediate_win(self,board: list[list[int]],legal_moves: list[tuple[int, int]],player: int,) -> tuple[int, int] | None:
        for r, c in legal_moves:
            board[r][c] = player
            winner = self._check_fast_winner(board)
            board[r][c] = EMPTY
            if winner == player:
                return (r, c)
        return None