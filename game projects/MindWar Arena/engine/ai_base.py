# engine/ai_base.py
from __future__ import annotations
import random
import threading
from typing import Any, TypeVar
from engine.core.event_manager import get_event_manager
from engine.interfaces.ai_interface import AIInterface
from engine.utils.constants import Difficulty, EventType
_MoveT = TypeVar("_MoveT")
class AIBase(AIInterface):
    def __init__(self,player: int,difficulty: Difficulty = Difficulty.BEGINNER,is_async: bool = True,) -> None:
        self.player: int = player
        self._difficulty: Difficulty = difficulty
        self.is_async: bool = is_async
        self._thinking: bool = False
        self._pending_move: object | None = None
        self._search_thread: threading.Thread | None = None
        self._search_generation: int = 0
        self._lock: threading.Lock = threading.Lock()
        self.event_manager = get_event_manager()
    def initialize(self) -> None:
        pass
    def reset(self) -> None:
        with self._lock:
            self._search_generation += 1
            if self._thinking:
                self.event_manager.emit(EventType.ON_AI_THINKING_END)
            self._thinking = False
            self._pending_move = None
            self._search_thread = None
    def get_difficulty(self) -> Difficulty:
        return self._difficulty
    def set_difficulty(self, difficulty: Difficulty) -> None:
        if not isinstance(difficulty, Difficulty):
            raise ValueError(f"Expected Difficulty enum, got {type(difficulty)}")
        self._difficulty = difficulty
    def select_action(self, game_state: dict[str, Any]) -> Any | None:
        legal_moves = game_state.get("legal_moves", [])
        if not legal_moves:
            return None
        if self._difficulty == Difficulty.BEGINNER:
            return self._select_beginner_move(game_state, legal_moves)
        if self._difficulty == Difficulty.EASY:
            return self._select_easy_move(game_state, legal_moves)
        if self._difficulty == Difficulty.MEDIUM:
            return self._select_medium_move(game_state, legal_moves)
        if self._difficulty == Difficulty.HARD:
            return self._select_hard_move(game_state, legal_moves)
        if self._difficulty == Difficulty.IMPOSSIBLE:
            return self._select_impossible_move(game_state, legal_moves)
        return self._select_random_move(legal_moves)
    def get_action(self, game: Any) -> Any | None:
        if game is None or game.is_game_over():
            return None
        with self._lock:
            if self._pending_move is not None:
                move = self._pending_move
                self._pending_move = None
                self.event_manager.emit(EventType.ON_AI_THINKING_END)
                return move
            if self._thinking:
                return None
        if not self.is_async:
            return self.select_action(game.get_state())
        self.select_action_async(game.get_state())
        return None
    def get_move(self, game: Any) -> Any | None:
        return self.get_action(game)
    def compute_move(self, game: Any) -> Any | None:
        return self.get_action(game)
    def select_action_async(self,game_state: dict[str, Any],) -> None:
        with self._lock:
            if self._thinking:
                return
            self._thinking = True
            current_gen = self._search_generation
        self.event_manager.emit(EventType.ON_AI_THINKING_START)
        def _worker() -> None:
            try:
                move = self.select_action(game_state)
                with self._lock:
                    if self._search_generation == current_gen:
                        self._pending_move = move
            except Exception as exc:
                import logging
                logging.getLogger(__name__).exception("Error in AI async worker: %s", exc)
            finally:
                with self._lock:
                    if self._search_generation == current_gen:
                        self._thinking = False
                        if self._pending_move is None:
                            self.event_manager.emit(EventType.ON_AI_THINKING_END)
        self._search_thread = threading.Thread(target=_worker, daemon=True)
        self._search_thread.start()
    @property
    def is_thinking(self) -> bool:
        with self._lock:
            return self._thinking
    def _select_beginner_move(self,game_state: dict[str, Any],legal_moves: list[Any],) -> Any | None:
        return self._select_random_move(legal_moves)
    def _select_easy_move(self,game_state: dict[str, Any],legal_moves: list[Any],) -> Any | None:
        if random.random() < 0.7:
            return self._select_beginner_move(game_state, legal_moves)
        return self._select_hard_move(game_state, legal_moves)
    def _select_medium_move(self,game_state: dict[str, Any],legal_moves: list[Any],) -> Any | None:
        if random.random() < 0.3:
            return self._select_beginner_move(game_state, legal_moves)
        return self._select_hard_move(game_state, legal_moves)
    def _select_hard_move(self,game_state: dict[str, Any],legal_moves: list[Any],) -> Any | None:
        return self._select_random_move(legal_moves)
    def _select_impossible_move(self,game_state: dict[str, Any],legal_moves: list[Any],) -> Any | None:
        return self._select_random_move(legal_moves)
    @staticmethod
    def _select_random_move(legal_moves: list[_MoveT]) -> _MoveT | None:
        if not legal_moves:
            return None
        return random.choice(legal_moves)
    def set_player(self, player: int) -> None:
        self.player = player
    def get_player(self) -> int:
        return self.player