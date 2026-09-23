# engine/ai/transposition_table.py
from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum
from typing import Any
class TTFlag(IntEnum):
    EXACT = 0
    LOWER = 1
    UPPER = 2
@dataclass(slots=True)
class TTEntry:
    hash_key: int = 0
    depth: int = 0
    score: float = 0.0
    flag: TTFlag = TTFlag.EXACT
    best_move: Any = None
    age: int = 0
class TranspositionTable:
    def __init__(self, size_mb: int = 32) -> None:
        self.capacity: int = max(1, (size_mb * 1024 * 1024) // 64)
        self._table: dict[int, TTEntry] = {}
        self.generation: int = 0
        self._hits: int = 0
        self._misses: int = 0
        self._collisions: int = 0
    def store(self,hash_key: int,depth: int,score: float,flag: TTFlag,best_move: Any = None,) -> None:
        index = hash_key % self.capacity
        existing = self._table.get(index)
        if existing is not None:
            if (existing.hash_key == hash_key and existing.depth > depth and existing.age == self.generation):
                return
            if existing.hash_key != hash_key:
                self._collisions += 1
        self._table[index] = TTEntry(hash_key=hash_key,depth=depth,score=score,flag=flag,best_move=best_move,age=self.generation,)
    def probe(self, hash_key: int) -> TTEntry | None:
        index = hash_key % self.capacity
        entry = self._table.get(index)
        if entry is None:
            self._misses += 1
            return None
        if entry.hash_key != hash_key:
            self._misses += 1
            return None
        self._hits += 1
        return entry
    def lookup_score(self,hash_key: int,depth: int,alpha: float,beta: float,) -> float | None:
        entry = self.probe(hash_key)
        if entry is None:
            return None
        if entry.depth < depth:
            return None
        if entry.flag == TTFlag.EXACT:
            return entry.score
        if entry.flag == TTFlag.LOWER and entry.score >= beta:
            return entry.score
        if entry.flag == TTFlag.UPPER and entry.score <= alpha:
            return entry.score
        return None
    def get_best_move(self, hash_key: int) -> Any:
        entry = self.probe(hash_key)
        if entry is not None:
            return entry.best_move
        return None
    def new_search(self) -> None:
        self.generation += 1
    def clear(self) -> None:
        self._table.clear()
        self.generation = 0
        self._hits = 0
        self._misses = 0
        self._collisions = 0
    @property
    def size(self) -> int:
        return len(self._table)
    @property
    def hit_rate(self) -> float:
        total = self._hits + self._misses
        if total == 0:
            return 0.0
        return self._hits / total
    def get_stats(self) -> dict[str, Any]:
        return {"hits": self._hits,"misses": self._misses,"collisions": self._collisions,"size": self.size,"capacity": self.capacity,"hit_rate": self.hit_rate,}