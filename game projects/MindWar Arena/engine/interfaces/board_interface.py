# engine/interfaces/board_interface.py
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
class BoardInterface(ABC):
    @abstractmethod
    def reset(self) -> None:
        pass
    @abstractmethod
    def copy(self) -> BoardInterface:
        pass
    @abstractmethod
    def get_cell(self, *position: int) -> int:
        pass
    @abstractmethod
    def set_cell(self, *args: int) -> bool:
        pass
    @abstractmethod
    def is_valid_position(self, *position: int) -> bool:
        pass
    @abstractmethod
    def is_cell_empty(self, *position: int) -> bool:
        pass
    @abstractmethod
    def get_board_state(self) -> Any:
        pass
    @abstractmethod
    def get_board_hash(self) -> int:
        pass
    @abstractmethod
    def is_board_full(self) -> bool:
        pass
    @abstractmethod
    def get_dimensions(self) -> tuple[int, ...]:
        pass
    @abstractmethod
    def make_move(self, *args: Any) -> bool:
        pass
    @abstractmethod
    def undo_move(self) -> bool:
        pass
    @abstractmethod
    def can_undo(self) -> bool:
        pass
    @abstractmethod
    def can_redo(self) -> bool:
        pass
    @abstractmethod
    def redo_move(self) -> bool:
        pass
    @abstractmethod
    def __str__(self) -> str:
        pass
    @abstractmethod
    def __eq__(self, other: object) -> bool:
        pass
    @abstractmethod
    def __hash__(self) -> int:
        pass