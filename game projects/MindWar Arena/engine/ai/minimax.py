# engine/ai/minimax.py
from __future__ import annotations
import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any
from engine.ai.transposition_table import TranspositionTable, TTFlag
GetMovesFunc = Callable[[Any], list[Any]]
ApplyMoveFunc = Callable[[Any, Any], Any]
UndoMoveFunc = Callable[[Any, Any], None]
EvaluateFunc = Callable[[Any], float]
IsTerminalFunc = Callable[[Any], bool]
MoveOrderFunc = Callable[[Any, list[Any]], list[Any]]
@dataclass
class SearchStats:
    nodes_evaluated: int = 0
    depth_reached: int = 0
    time_elapsed: float = 0.0
    cutoffs: int = 0
class MinimaxEngine:
    def __init__(self,get_moves: GetMovesFunc,apply_move: ApplyMoveFunc,evaluate: EvaluateFunc,is_terminal: IsTerminalFunc,undo_move: UndoMoveFunc | None = None,order_moves: MoveOrderFunc | None = None,transposition_table: TranspositionTable | None = None,get_hash: Callable[[Any], int] | None = None,) -> None:
        self.get_moves = get_moves
        self.apply_move = apply_move
        self.undo_move = undo_move
        self.evaluate = evaluate
        self.is_terminal = is_terminal
        self.order_moves = order_moves
        self.transposition_table = transposition_table
        self.get_hash = get_hash
        self._stats = SearchStats()
        self._time_limit: float = 0.0
        self._start_time: float = 0.0
        self._timed_out: bool = False
    def search(self,state: Any,depth: int = 4,maximise: bool = True,time_limit: float = 0.0,) -> Any | None:
        self._stats = SearchStats()
        if time_limit > 0:
            self._time_limit = time_limit
            self._start_time = time.perf_counter()
            self._timed_out = False
        elif self._time_limit <= 0:
            self._time_limit = 0.0
            self._start_time = time.perf_counter()
            self._timed_out = False
        moves = self.get_moves(state)
        if not moves:
            return None
        if self.transposition_table is not None:
            self.transposition_table.generation += 1
        if self.order_moves:
            moves = self.order_moves(state, moves)
        best_move: Any | None = None
        best_score = float("-inf") if maximise else float("inf")
        for move in moves:
            if self._check_timeout():
                break
            child = self._do_move(state, move)
            score = self._alpha_beta(child,depth - 1,float("-inf"),float("inf"),not maximise,)
            self._do_undo(state, move)
            if maximise:
                if score > best_score:
                    best_score = score
                    best_move = move
            else:
                if score < best_score:
                    best_score = score
                    best_move = move
        self._stats.time_elapsed = time.perf_counter() - self._start_time
        self._stats.depth_reached = depth
        return best_move
    def search_iterative(self,state: Any,max_depth: int = 10,maximise: bool = True,time_limit: float = 5.0,) -> Any | None:
        self._start_time = time.perf_counter()
        self._time_limit = time_limit
        self._timed_out = False
        best_move: Any | None = None
        for depth in range(1, max_depth + 1):
            if self._check_timeout():
                break
            move = self.search(state, depth, maximise, time_limit=0)
            if not self._timed_out and move is not None:
                best_move = move
            if self._timed_out:
                break
        return best_move
    @property
    def stats(self) -> SearchStats:
        return self._stats
    def _alpha_beta(self,state: Any,depth: int,alpha: float,beta: float,maximise: bool,) -> float:
        if self._check_timeout():
            return self.evaluate(state)
        if depth <= 0 or self.is_terminal(state):
            self._stats.nodes_evaluated += 1
            return self.evaluate(state)
        orig_alpha = alpha
        orig_beta = beta
        hash_key = None
        if self.transposition_table is not None:
            if self.get_hash is not None:
                hash_key = self.get_hash(state)
            elif hasattr(state, "get_hash"):
                hash_key = state.get_hash()
            elif hasattr(state, "get_zobrist_hash"):
                hash_key = state.get_zobrist_hash()
            elif isinstance(state, dict) and "hash" in state:
                hash_key = state["hash"]
            if hash_key is not None:
                cached_score = self.transposition_table.lookup_score(hash_key, depth, alpha, beta)
                if cached_score is not None:
                    self._stats.cutoffs += 1
                    return cached_score
        moves = self.get_moves(state)
        if not moves:
            self._stats.nodes_evaluated += 1
            return self.evaluate(state)
        if self.order_moves:
            moves = self.order_moves(state, moves)
        elif self.transposition_table is not None and hash_key is not None:
            best_tt_move = self.transposition_table.get_best_move(hash_key)
            if best_tt_move is not None and best_tt_move in moves:
                moves = [best_tt_move] + [m for m in moves if m != best_tt_move]
        best_move_local = None
        if maximise:
            value = float("-inf")
            for move in moves:
                child = self._do_move(state, move)
                score = self._alpha_beta(child, depth - 1, alpha, beta, False)
                self._do_undo(state, move)
                if score > value:
                    value = score
                    best_move_local = move
                alpha = max(alpha, value)
                if alpha >= beta:
                    self._stats.cutoffs += 1
                    break
        else:
            value = float("inf")
            for move in moves:
                child = self._do_move(state, move)
                score = self._alpha_beta(child, depth - 1, alpha, beta, True)
                self._do_undo(state, move)
                if score < value:
                    value = score
                    best_move_local = move
                beta = min(beta, value)
                if alpha >= beta:
                    self._stats.cutoffs += 1
                    break
        if self.transposition_table is not None and hash_key is not None:
            if value <= orig_alpha:
                flag = TTFlag.UPPER
            elif value >= orig_beta:
                flag = TTFlag.LOWER
            else:
                flag = TTFlag.EXACT
            self.transposition_table.store(hash_key, depth, value, flag, best_move=best_move_local)
        return value
    def _do_move(self, state: Any, move: Any) -> Any:
        return self.apply_move(state, move)
    def _do_undo(self, state: Any, move: Any) -> None:
        if self.undo_move is not None:
            self.undo_move(state, move)
    def _check_timeout(self) -> bool:
        if self._time_limit <= 0:
            return False
        elapsed = time.perf_counter() - self._start_time
        if elapsed >= self._time_limit:
            self._timed_out = True
            return True
        return False