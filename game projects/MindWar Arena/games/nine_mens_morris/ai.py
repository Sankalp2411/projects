# games/nine_mens_morris/ai.py
from __future__ import annotations
import random
from typing import Any
from engine.ai_base import AIBase
from engine.utils.constants import Difficulty
from games.nine_mens_morris.board import NineMensMorrisBoard
from games.nine_mens_morris.constants import (EMPTY,PHASE_PLACEMENT,PLAYER_BLACK,PLAYER_WHITE,)
from games.nine_mens_morris.rules import NineMensMorrisRules
class NineMensMorrisAI(AIBase):
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
    def select_action(self, game_state: dict[str, Any]) -> Any | None:
        if not self.initialized or not game_state:
            return None
        board_raw = game_state.get("board")
        if board_raw is None:
            return None
        board = NineMensMorrisBoard()
        board._board = list(board_raw)
        if game_state.get("capture_pending"):
            removable = NineMensMorrisRules.get_removable_pieces(board, self.player)
            if not removable:
                return None
            return self._select_removal(board, removable)
        phase = game_state.get("phase", PHASE_PLACEMENT)
        if phase == PHASE_PLACEMENT:
            available = board.get_available_positions()
            if not available:
                return None
            if self._difficulty == Difficulty.BEGINNER:
                return random.choice(available)
            elif self._difficulty == Difficulty.EASY:
                if random.random() < 0.70:
                    return random.choice(available)
                return self._select_placement(board, available)
            elif self._difficulty == Difficulty.MEDIUM:
                if random.random() < 0.30:
                    return random.choice(available)
                return self._select_placement(board, available)
            return self._select_placement(board, available)
        else:
            can_fly = game_state.get("flying", False) or NineMensMorrisRules.can_fly(board, self.player)
            legal_moves = self._get_moves(board, can_fly)
            if not legal_moves:
                return None
            if self._difficulty == Difficulty.BEGINNER:
                return random.choice(legal_moves)
            elif self._difficulty == Difficulty.EASY:
                if random.random() < 0.70:
                    return random.choice(legal_moves)
                return self._select_movement(board, legal_moves)
            elif self._difficulty == Difficulty.MEDIUM:
                if random.random() < 0.30:
                    return random.choice(legal_moves)
                return self._select_movement(board, legal_moves)
            return self._select_movement(board, legal_moves)
    def _select_removal(self, board: NineMensMorrisBoard, removable: list[int]) -> int:
        best_target = removable[0]
        max_threat = -1
        for pos in removable:
            threat = 0
            for mill in NineMensMorrisRules.get_mills_for_position(pos):
                count = sum(1 for c in mill if board.get_position(c) == self.opponent)
                if count == 2:
                    threat += 10
                elif count == 1:
                    threat += 2
            if threat > max_threat:
                max_threat = threat
                best_target = pos
        return best_target
    def _select_placement(self, board: NineMensMorrisBoard, available: list[int]) -> int:
        for pos in available:
            board._board[pos] = self.player
            if NineMensMorrisRules.is_mill(board, pos, self.player):
                board._board[pos] = EMPTY
                return pos
            board._board[pos] = EMPTY
        for pos in available:
            board._board[pos] = self.opponent
            if NineMensMorrisRules.is_mill(board, pos, self.opponent):
                board._board[pos] = EMPTY
                return pos
            board._board[pos] = EMPTY
        best_pos = None
        max_threats = -1
        for pos in available:
            board._board[pos] = self.player
            threats = 0
            for mill in NineMensMorrisRules.get_mills_for_position(pos):
                count_own = sum(1 for c in mill if board.get_position(c) == self.player)
                count_empty = sum(1 for c in mill if board.get_position(c) == EMPTY)
                if count_own == 2 and count_empty == 1:
                    threats += 1
            board._board[pos] = EMPTY
            if threats > max_threats:
                max_threats = threats
                best_pos = pos
        if best_pos is not None and max_threats > 0:
            return best_pos
        best_pos = available[0]
        max_adj = -1
        for pos in available:
            adj_count = len(NineMensMorrisRules.get_adjacent_positions(pos))
            if adj_count > max_adj:
                max_adj = adj_count
                best_pos = pos
        return best_pos
    def _select_movement(self,board: NineMensMorrisBoard,legal_moves: list[tuple[int, int]],) -> tuple[int, int]:
        for src, dst in legal_moves:
            board._board[src] = EMPTY
            board._board[dst] = self.player
            forms_mill = NineMensMorrisRules.is_mill(board, dst, self.player)
            board._board[dst] = EMPTY
            board._board[src] = self.player
            if forms_mill:
                return (src, dst)
        safe_moves = []
        for src, dst in legal_moves:
            board._board[src] = EMPTY
            board._board[dst] = self.player
            opp_moves = NineMensMorrisRules.get_legal_moves(board, self.opponent)
            opp_can_mill = False
            for os, od in opp_moves:
                board._board[os] = EMPTY
                board._board[od] = self.opponent
                if NineMensMorrisRules.is_mill(board, od, self.opponent):
                    opp_can_mill = True
                board._board[od] = EMPTY
                board._board[os] = self.opponent
                if opp_can_mill:
                    break
            board._board[dst] = EMPTY
            board._board[src] = self.player
            if not opp_can_mill:
                safe_moves.append((src, dst))
        candidates = safe_moves if safe_moves else legal_moves
        best_score = -float("inf")
        best_move = candidates[0]
        for src, dst in candidates:
            score = 0.0
            board._board[src] = EMPTY
            board._board[dst] = self.player
            for mill in NineMensMorrisRules.get_mills_for_position(dst):
                count_own = sum(1 for c in mill if board.get_position(c) == self.player)
                count_empty = sum(1 for c in mill if board.get_position(c) == EMPTY)
                if count_own == 2 and count_empty == 1:
                    score += 15.0
            adj_empty = sum(1 for adj in NineMensMorrisRules.get_adjacent_positions(dst) if board.is_position_empty(adj))
            score += adj_empty * 2.0
            board._board[dst] = EMPTY
            board._board[src] = self.player
            if score > best_score:
                best_score = score
                best_move = (src, dst)
        return best_move
    def _get_moves(self, board: NineMensMorrisBoard, can_fly: bool) -> list[tuple[int, int]]:
        moves = []
        player_positions = board.get_player_positions(self.player)
        available = board.get_available_positions()
        for src in player_positions:
            if can_fly:
                for dst in available:
                    moves.append((src, dst))
            else:
                for dst in NineMensMorrisRules.get_adjacent_positions(src):
                    if board.is_position_empty(dst):
                        moves.append((src, dst))
        return moves