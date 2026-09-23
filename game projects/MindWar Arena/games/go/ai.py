# games/go/ai.py
from __future__ import annotations
import random
from typing import Any
from engine.ai_base import AIBase
from engine.utils.constants import Difficulty
from games.go.board import GoBoard
from games.go.constants import (ACTION_PASS,BOARD_COLUMNS,BOARD_ROWS,PLAYER_BLACK,PLAYER_WHITE,)
from games.go.rules import GoRules
class GoAI(AIBase):
    def __init__(self,player: int,difficulty: Difficulty = Difficulty.MEDIUM,) -> None:
        super().__init__(player=player, difficulty=difficulty)
        self.opponent = PLAYER_BLACK if player == PLAYER_WHITE else PLAYER_WHITE
        self.initialized = False
    def initialize(self) -> None:
        self.initialized = True
    def reset(self) -> None:
        super().reset()
        self.initialized = False
    def set_player(self, player: int) -> None:
        super().set_player(player)
        self.opponent = PLAYER_BLACK if player == PLAYER_WHITE else PLAYER_WHITE
    def select_action(self, game_state: dict[str, Any]) -> Any | None:
        if not self.initialized or not game_state:
            return None
        board_state = game_state.get("board")
        if board_state is None:
            return None
        current_player = game_state.get("current_player")
        if current_player != self.player:
            return None
        board = GoBoard()
        board.set_board_state(board_state)
        ko_pos = game_state.get("ko_position")
        if not (isinstance(ko_pos, tuple) and len(ko_pos) == 2):
            ko_pos = None
        legal_moves = GoRules.get_legal_moves(board, self.player, ko_pos)
        if not legal_moves:
            return ACTION_PASS
        if self._difficulty == Difficulty.BEGINNER:
            return random.choice(legal_moves)
        elif self._difficulty == Difficulty.EASY:
            if random.random() < 0.70:
                return random.choice(legal_moves)
            return self._select_hard_move(board, legal_moves, ko_pos)
        elif self._difficulty == Difficulty.MEDIUM:
            if random.random() < 0.30:
                return random.choice(legal_moves)
            return self._select_hard_move(board, legal_moves, ko_pos)
        elif self._difficulty == Difficulty.HARD:
            return self._select_hard_move(board, legal_moves, ko_pos)
        else:
            return self._select_impossible_move(board, legal_moves, ko_pos)
    def _evaluate_candidate_move(self,board: GoBoard,move: tuple[int, int],ko_position: tuple[int, int] | None = None,) -> float:
        r, c = move
        score = 0.0
        test_board = board.copy()
        if not GoRules.apply_move(test_board, r, c, self.player, ko_position):
            return -9999.0
        curr_opp = test_board.count_stones(self.opponent)
        prev_opp = board.count_stones(self.opponent)
        captured = prev_opp - curr_opp
        score += captured * 60.0
        own_group = GoRules.get_group(test_board, r, c)
        own_liberties = len(GoRules.get_group_liberties(test_board, own_group))
        score += min(own_liberties, 4) * 4.0
        for nr, nc in GoRules.get_neighbors(r, c):
            if board.get_cell(nr, nc) == self.player:
                prev_grp = GoRules.get_group(board, nr, nc)
                if len(GoRules.get_group_liberties(board, prev_grp)) == 1:
                    if own_liberties >= 2:
                        score += 40.0
        for nr, nc in GoRules.get_neighbors(r, c):
            if test_board.get_cell(nr, nc) == self.opponent:
                opp_grp = GoRules.get_group(test_board, nr, nc)
                if len(GoRules.get_group_liberties(test_board, opp_grp)) == 1:
                    score += 25.0
        territory = GoRules.count_territory(test_board, self.player)
        score += territory * 4.0
        center_dist = abs(r - BOARD_ROWS // 2) + abs(c - BOARD_COLUMNS // 2)
        score -= center_dist * 0.3
        score += random.uniform(-0.05, 0.05)
        return score
    def _select_hard_move(self,board: GoBoard,legal_moves: list[tuple[int, int]],ko_position: tuple[int, int] | None,) -> tuple[int, int]:
        best_score = -float("inf")
        best_moves: list[tuple[int, int]] = []
        for move in legal_moves:
            s = self._evaluate_candidate_move(board, move, ko_position)
            if s > best_score:
                best_score = s
                best_moves = [move]
            elif abs(s - best_score) < 1e-4:
                best_moves.append(move)
        return random.choice(best_moves) if best_moves else random.choice(legal_moves)
    def _select_impossible_move(self,board: GoBoard,legal_moves: list[tuple[int, int]],ko_position: tuple[int, int] | None,) -> tuple[int, int]:
        best_score = -float("inf")
        best_moves: list[tuple[int, int]] = []
        for move in legal_moves:
            s = self._evaluate_candidate_move(board, move, ko_position)
            test_board = board.copy()
            if GoRules.apply_move(test_board, move[0], move[1], self.player, ko_position):
                opp_moves = GoRules.get_legal_moves(test_board, self.opponent, None)
                if opp_moves:
                    worst_opp_threat = 0.0
                    for om in opp_moves[:8]:
                        hypo_board = test_board.copy()
                        if GoRules.apply_move(hypo_board, om[0], om[1], self.opponent, None):
                            hypo_own = hypo_board.count_stones(self.player)
                            now_own = test_board.count_stones(self.player)
                            if now_own - hypo_own > 0:
                                worst_opp_threat = max(worst_opp_threat, (now_own - hypo_own) * 30.0)
                    s -= worst_opp_threat
            if s > best_score:
                best_score = s
                best_moves = [move]
            elif abs(s - best_score) < 1e-4:
                best_moves.append(move)
        return random.choice(best_moves) if best_moves else random.choice(legal_moves)
    def get_action(self, game: Any) -> Any | None:
        return self.select_action(game.get_state())
    def learn(self,state: Any,action: Any,reward: Any,next_state: Any,) -> None:
        pass