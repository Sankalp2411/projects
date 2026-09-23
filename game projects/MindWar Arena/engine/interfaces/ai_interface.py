# engine/interfaces/ai_interface.py
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
from engine.utils.constants import Difficulty
AIDifficulty = Difficulty
class AIInterface(ABC):
    @abstractmethod
    def initialize(self) -> None:
        pass
    @abstractmethod
    def reset(self) -> None:
        pass
    @abstractmethod
    def select_action(self, game_state: dict[str, Any]) -> Any | None:
        pass
    def get_difficulty(self) -> Difficulty:
        return getattr(self, "_difficulty", Difficulty.MEDIUM)
    def set_difficulty(self, difficulty: Difficulty) -> None:
        self._difficulty = difficulty
    def learn(self,state: Any,action: Any,reward: float,next_state: Any,) -> None:
        pass
    def evaluate_position(self, game_state: dict[str, Any]) -> float:
        return 0.0