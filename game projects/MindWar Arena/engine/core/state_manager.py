# engine/core/state_manager.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
@dataclass
class MoveRecord:
    move: Any = None
    player: int = 0
    captured_pieces: list[tuple[int, ...]] = field(default_factory=list)
    previous_state: dict[str, Any] = field(default_factory=dict)
    before_state: dict[str, Any] = field(default_factory=dict)
    after_state: dict[str, Any] = field(default_factory=dict)
    promoted_from: int | None = None
    promoted_to: int | None = None
    extra: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
class StateManager:
    def __init__(self, max_history: int = 10_000) -> None:
        self._history: list[MoveRecord] = []
        self._redo_stack: list[MoveRecord] = []
        self._max_history: int = max_history
    def push(self, record: MoveRecord) -> None:
        self._history.append(record)
        self._redo_stack.clear()
        if len(self._history) > self._max_history:
            excess = len(self._history) - self._max_history
            del self._history[:excess]
    def record_move(self, record: MoveRecord) -> None:
        self.push(record)
    def undo(self) -> MoveRecord | None:
        if not self._history:
            return None
        record = self._history.pop()
        self._redo_stack.append(record)
        return record
    def redo(self) -> MoveRecord | None:
        if not self._redo_stack:
            return None
        record = self._redo_stack.pop()
        self._history.append(record)
        return record
    def can_undo(self) -> bool:
        return bool(self._history)
    def can_redo(self) -> bool:
        return bool(self._redo_stack)
    def peek(self) -> MoveRecord | None:
        return self._history[-1] if self._history else None
    def peek_redo(self) -> MoveRecord | None:
        return self._redo_stack[-1] if self._redo_stack else None
    @property
    def move_count(self) -> int:
        return len(self._history)
    @property
    def redo_count(self) -> int:
        return len(self._redo_stack)
    def get_history(self) -> list[MoveRecord]:
        return list(self._history)
    def clear(self) -> None:
        self._history.clear()
        self._redo_stack.clear()
    def reset(self) -> None:
        self.clear()