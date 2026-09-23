# engine/ai/mcts.py
from __future__ import annotations
import math
import random
import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any
from engine.utils.constants import AI_MCTS_EXPLORATION_CONSTANT
GetMovesFunc = Callable[[Any], list[Any]]
ApplyMoveFunc = Callable[[Any, Any], Any]
IsTerminalFunc = Callable[[Any], bool]
GetResultFunc = Callable[[Any, int], float]
class MCTSNode:
    __slots__ = ("state","parent","move","player","children","untried_moves","visits","wins",)
    def __init__(self,state: Any,parent: MCTSNode | None = None,move: Any = None,player: int = 0,untried_moves: list[Any] | None = None,) -> None:
        self.state = state
        self.parent = parent
        self.move = move
        self.player = player
        self.children: list[MCTSNode] = []
        self.untried_moves: list[Any] = untried_moves or []
        self.visits: int = 0
        self.wins: float = 0.0
    def uct_value(self, exploration: float = AI_MCTS_EXPLORATION_CONSTANT) -> float:
        if self.visits == 0:
            return float("inf")
        parent_visits = self.parent.visits if self.parent else 1
        exploitation = self.wins / self.visits
        exploration_term = exploration * math.sqrt(math.log(parent_visits) / self.visits)
        return exploitation + exploration_term
    def is_fully_expanded(self) -> bool:
        return len(self.untried_moves) == 0
    def best_child(self, exploration: float = AI_MCTS_EXPLORATION_CONSTANT) -> MCTSNode:
        return max(self.children, key=lambda c: c.uct_value(exploration))
    def most_visited_child(self) -> MCTSNode | None:
        if not self.children:
            return None
        return max(self.children, key=lambda c: c.visits)
@dataclass
class MCTSStats:
    iterations: int = 0
    time_elapsed: float = 0.0
    max_depth: int = 0
class MCTSEngine:
    def __init__(self,get_moves: GetMovesFunc,apply_move: ApplyMoveFunc,is_terminal: IsTerminalFunc,get_result: GetResultFunc,get_current_player: Callable[[Any], int] | None = None,exploration: float = AI_MCTS_EXPLORATION_CONSTANT,copy_state: Callable[[Any], Any] | None = None,) -> None:
        from copy import deepcopy
        self.get_moves = get_moves
        self.apply_move = apply_move
        self.is_terminal = is_terminal
        self.get_result = get_result
        self.get_current_player = get_current_player
        self.exploration = exploration
        self.copy_state = copy_state or (lambda s: s.copy() if hasattr(s, "copy") else deepcopy(s))
        self._stats = MCTSStats()
    def search(self,state: Any,player: int,iterations: int = 1000,time_limit: float = 0.0,) -> Any | None:
        start_time = time.perf_counter()
        self._stats = MCTSStats()
        moves = self.get_moves(state)
        if not moves:
            return None
        root = MCTSNode(state=state,player=player,untried_moves=list(moves),)
        for i in range(iterations):
            if time_limit > 0:
                if time.perf_counter() - start_time >= time_limit:
                    break
            node = self._select(root)
            if not self.is_terminal(node.state) and node.untried_moves:
                node = self._expand(node)
            result = self._simulate(node.state, player)
            self._backpropagate(node, result, player)
            self._stats.iterations = i + 1
        self._stats.time_elapsed = time.perf_counter() - start_time
        best = root.most_visited_child()
        return best.move if best else None
    @property
    def stats(self) -> MCTSStats:
        return self._stats
    def _select(self, node: MCTSNode) -> MCTSNode:
        while node.is_fully_expanded() and node.children:
            if self.is_terminal(node.state):
                break
            node = node.best_child(self.exploration)
        return node
    def _expand(self, node: MCTSNode) -> MCTSNode:
        move = node.untried_moves.pop(random.randrange(len(node.untried_moves)))
        child_state = self.apply_move(self.copy_state(node.state), move)
        child_moves = self.get_moves(child_state)
        child_player = node.player
        if self.get_current_player is not None:
            child_player = self.get_current_player(child_state)
        child = MCTSNode(state=child_state,parent=node,move=move,player=child_player,untried_moves=child_moves,)
        node.children.append(child)
        return child
    def _simulate(self, state: Any, root_player: int) -> float:
        current = self.copy_state(state)
        depth = 0
        max_rollout = 500
        while not self.is_terminal(current) and depth < max_rollout:
            moves = self.get_moves(current)
            if not moves:
                break
            move = random.choice(moves)
            current = self.apply_move(current, move)
            depth += 1
        self._stats.max_depth = max(self._stats.max_depth, depth)
        return self.get_result(current, root_player)
    def _backpropagate(self,node: MCTSNode,result: float,root_player: int,) -> None:
        current: MCTSNode | None = node
        while current is not None:
            current.visits += 1
            if current.player == root_player:
                current.wins += result
            else:
                current.wins -= result
            current = current.parent