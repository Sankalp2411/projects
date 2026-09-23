# engine/board/graph_board.py
from __future__ import annotations
import random
from typing import Any
from engine.interfaces.board_interface import BoardInterface
class GraphBoard(BoardInterface):
    def __init__(self,num_nodes: int = 24,adjacency: dict[int, list[int]] | None = None,empty_value: int = 0,*,num_piece_types: int = 4,) -> None:
        self.num_nodes: int = num_nodes
        self.empty_value: int = empty_value
        self.adjacency: dict[int, list[int]] = adjacency or {}
        self._nodes: dict[int, int] = {}
        self._move_stack: list[dict[str, Any]] = []
        self._redo_stack: list[dict[str, Any]] = []
        self._num_piece_types: int = num_piece_types
        self._zobrist_table: dict[int, list[int]] = {}
        self._zobrist_hash: int = 0
        self._init_zobrist()
        self.reset()
    def _init_zobrist(self) -> None:
        rng = random.Random(777)
        for node_id in range(self.num_nodes):
            self._zobrist_table[node_id] = [rng.getrandbits(64) for _ in range(self._num_piece_types)]
    def _update_zobrist(self, node: int, old_val: int, new_val: int) -> None:
        if old_val != self.empty_value and old_val < self._num_piece_types:
            self._zobrist_hash ^= self._zobrist_table[node][old_val]
        if new_val != self.empty_value and new_val < self._num_piece_types:
            self._zobrist_hash ^= self._zobrist_table[node][new_val]
    def reset(self) -> None:
        self._nodes = {i: self.empty_value for i in range(self.num_nodes)}
        self._move_stack.clear()
        self._redo_stack.clear()
        self._zobrist_hash = 0
    def copy(self) -> GraphBoard:
        new_board = GraphBoard(self.num_nodes,adjacency={k: list(v) for k, v in self.adjacency.items()},empty_value=self.empty_value,num_piece_types=self._num_piece_types,)
        new_board._nodes = dict(self._nodes)
        new_board._zobrist_hash = self._zobrist_hash
        new_board._zobrist_table = self._zobrist_table
        return new_board
    def get_cell(self, node: int, *_: int) -> int:
        return self._nodes.get(node, self.empty_value)
    def set_cell(self, node: int, value: int, *_: int) -> bool:
        if not self.is_valid_position(node):
            return False
        old = self._nodes[node]
        self._nodes[node] = value
        self._update_zobrist(node, old, value)
        return True
    def is_valid_position(self, node: int, *_: int) -> bool:
        return 0 <= node < self.num_nodes
    def is_cell_empty(self, node: int, *_: int) -> bool:
        return self._nodes.get(node, self.empty_value) == self.empty_value
    def get_neighbors(self, node: int) -> list[int]:
        return self.adjacency.get(node, [])
    def are_adjacent(self, node_a: int, node_b: int) -> bool:
        return node_b in self.adjacency.get(node_a, [])
    def add_edge(self, node_a: int, node_b: int, bidirectional: bool = True) -> None:
        if node_a not in self.adjacency:
            self.adjacency[node_a] = []
        if node_b not in self.adjacency[node_a]:
            self.adjacency[node_a].append(node_b)
        if bidirectional:
            if node_b not in self.adjacency:
                self.adjacency[node_b] = []
            if node_a not in self.adjacency[node_b]:
                self.adjacency[node_b].append(node_a)
    def get_player_nodes(self, player: int) -> list[int]:
        return [n for n, v in self._nodes.items() if v == player]
    def count_pieces(self, player: int) -> int:
        return sum(1 for v in self._nodes.values() if v == player)
    def get_empty_nodes(self) -> list[int]:
        return [n for n, v in self._nodes.items() if v == self.empty_value]
    def get_board_state(self) -> dict[int, int]:
        return dict(self._nodes)
    def get_board_hash(self) -> int:
        return self._zobrist_hash
    def is_board_full(self) -> bool:
        return all(v != self.empty_value for v in self._nodes.values())
    def get_dimensions(self) -> tuple[int]:
        return (self.num_nodes,)
    def make_move(self,node: int,value: int,*,removed_from: int | None = None,removed_value: int | None = None,extra: dict[str, Any] | None = None,) -> bool:
        if not self.is_valid_position(node):
            return False
        record: dict[str, Any] = {"node": node,"old_value": self._nodes[node],"new_value": value,}
        if removed_from is not None:
            record["removed_from"] = removed_from
            record["removed_value"] = (removed_value if removed_value is not None else self._nodes.get(removed_from, self.empty_value))
        if extra:
            record["extra"] = extra
        if removed_from is not None:
            self.set_cell(removed_from, self.empty_value)
        self.set_cell(node, value)
        self._move_stack.append(record)
        self._redo_stack.clear()
        return True
    def undo_move(self) -> bool:
        if not self._move_stack:
            return False
        record = self._move_stack.pop()
        self.set_cell(record["node"], record["old_value"])
        if "removed_from" in record:
            self.set_cell(record["removed_from"], record["removed_value"])
        self._redo_stack.append(record)
        return True
    def redo_move(self) -> bool:
        if not self._redo_stack:
            return False
        record = self._redo_stack.pop()
        if "removed_from" in record:
            self.set_cell(record["removed_from"], self.empty_value)
        self.set_cell(record["node"], record["new_value"])
        self._move_stack.append(record)
        return True
    def can_undo(self) -> bool:
        return bool(self._move_stack)
    def can_redo(self) -> bool:
        return bool(self._redo_stack)
    def __str__(self) -> str:
        return " | ".join(f"{n}:{self._nodes[n]}" for n in sorted(self._nodes))
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GraphBoard):
            return NotImplemented
        return self._nodes == other._nodes
    def __hash__(self) -> int:
        return self._zobrist_hash