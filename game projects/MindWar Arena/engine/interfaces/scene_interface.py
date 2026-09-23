# engine/interfaces/scene_interface.py
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from engine.game_manager import GameManager
class SceneInterface(ABC):
    @abstractmethod
    def enter(self) -> None:
        pass
    @abstractmethod
    def exit(self) -> None:
        pass
    @abstractmethod
    def update(self) -> None:
        pass
    @abstractmethod
    def render(self) -> None:
        pass
    @abstractmethod
    def handle_event(self, event: object) -> None:
        pass
    @abstractmethod
    def set_game_manager(self, game_manager: GameManager) -> None:
        pass