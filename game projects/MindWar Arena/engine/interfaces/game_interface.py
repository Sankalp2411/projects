# engine/interfaces/game_interface.py
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
class GameInterface(ABC):
    @abstractmethod
    def initialize(self) -> None:
        pass
    @abstractmethod
    def reset(self) -> None:
        pass
    @abstractmethod
    def shutdown(self) -> None:
        pass
    @abstractmethod
    def update(self) -> None:
        pass
    @abstractmethod
    def render(self) -> None:
        pass
    @abstractmethod
    def get_state(self) -> dict[str, Any]:
        pass
    @abstractmethod
    def get_board(self) -> Any:
        pass
    @abstractmethod
    def get_current_player(self) -> int:
        pass
    @abstractmethod
    def get_winner(self) -> int | None:
        pass
    @abstractmethod
    def is_game_over(self) -> bool:
        pass
    @abstractmethod
    def make_move(self, *args: Any, **kwargs: Any) -> bool:
        pass
    @abstractmethod
    def get_legal_moves(self) -> list[Any]:
        pass
    def get_valid_moves(self) -> list[Any]:
        return self.get_legal_moves()
    def can_undo(self) -> bool:
        return False
    def undo(self) -> bool:
        return False
    def can_redo(self) -> bool:
        return False
    def redo(self) -> bool:
        return False
    def get_hint(self) -> Any | None:
        return None
    def get_valid_moves_for_cell(self,*position: int,) -> list[Any]:
        all_moves = self.get_legal_moves()
        if not position:
            return all_moves
        result: list[Any] = []
        for move in all_moves:
            if isinstance(move, tuple) and len(move) >= len(position):
                if move[: len(position)] == position:
                    result.append(move)
        return result
    def serialize(self) -> str:
        return ""
    def deserialize(self, data: str) -> bool:
        return False