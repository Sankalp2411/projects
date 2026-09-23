# engine/game_base.py
from __future__ import annotations
from typing import Any
from engine.core.event_manager import EventManager, get_event_manager
from engine.core.state_manager import MoveRecord, StateManager
from engine.interfaces.game_interface import GameInterface
from engine.interfaces.game_result import GameResult
from engine.utils.constants import Difficulty, EventType, GameMode, GameState
class GameBase(GameInterface):
    def __init__(self,renderer: Any,game_mode: int = GameMode.HUMAN_VS_HUMAN,difficulty: Difficulty = Difficulty.MEDIUM,) -> None:
        self.renderer: Any = renderer
        self.game_mode: int = game_mode
        self.difficulty: Difficulty = difficulty
        self.board: Any = None
        self.current_player: int = 1
        self.next_starting_player: int = 1
        self.result: GameResult = GameResult()
        self.game_state: int = GameState.NOT_STARTED
        self.move_count: int = 0
        self.state_manager: StateManager = StateManager(max_history=100)
        self.event_manager: EventManager = get_event_manager()
        self.board_renderer: Any = None
        self.overlay_renderer: Any = None
        self.human_player: Any = None
        self.ai: Any = None
    def initialize(self) -> None:
        if hasattr(self, "ai") and self.ai is not None:
            if hasattr(self.ai, "initialize"):
                self.ai.initialize()
        self.reset()
    def reset(self) -> None:
        if self.board is not None and hasattr(self.board, "reset"):
            self.board.reset()
        self.current_player = self.choose_starting_player()
        self.result.reset()
        self.game_state = GameState.RUNNING
        self.move_count = 0
        self.state_manager.clear()
        if hasattr(self, "human_player") and self.human_player is not None:
            if hasattr(self.human_player, "reset"):
                self.human_player.reset()
        if hasattr(self, "ai") and self.ai is not None:
            if hasattr(self.ai, "reset"):
                self.ai.reset()
        if self.board_renderer is not None and hasattr(self.board_renderer, "reset"):
            self.board_renderer.reset()
        if self.overlay_renderer is not None and hasattr(self.overlay_renderer, "reset"):
            self.overlay_renderer.reset()
        self.event_manager.emit(EventType.ON_GAME_RESET)
    def shutdown(self) -> None:
        pass
    def set_difficulty(self, difficulty: Difficulty) -> None:
        self.difficulty = difficulty
        if hasattr(self, "ai") and self.ai is not None:
            if hasattr(self.ai, "set_difficulty"):
                self.ai.set_difficulty(difficulty)
    def choose_starting_player(self) -> int:
        player = self.next_starting_player
        self.next_starting_player = 2 if player == 1 else 1
        return player
    def update(self) -> None:
        if self.is_frozen():
            return
        self.update_current_player()
    def update_current_player(self) -> None:
        controller = self.get_current_controller()
        if controller is None:
            return
        action = controller.get_action(self)
        if action is not None:
            self.make_move(action)
    def get_current_controller(self) -> Any:
        if self.game_mode == GameMode.HUMAN_VS_HUMAN:
            return self.human_player
        if self.game_mode == GameMode.HUMAN_VS_AI:
            return self.human_player if self.current_player == 1 else self.ai
        if self.game_mode == GameMode.AI_VS_AI:
            return self.ai
        return None
    def render(self) -> None:
        if self.board_renderer is not None:
            self.board_renderer.render(self)
        if self.overlay_renderer is not None:
            self.overlay_renderer.render(self)
    def can_undo(self) -> bool:
        return self.state_manager.can_undo()
    def can_redo(self) -> bool:
        return self.state_manager.can_redo()
    def undo(self) -> bool:
        if not self.can_undo():
            return False
        steps = (2 if (self.game_mode == GameMode.HUMAN_VS_AI and self.state_manager.move_count >= 2 and not self.is_game_over()) else 1)
        undone = False
        for _ in range(steps):
            record = self.state_manager.undo()
            if record is None:
                break
            if self._apply_undo_record(record):
                self.move_count = max(0, self.move_count - 1)
                self.current_player = record.player
                undone = True
        if undone:
            self.result.reset()
            self.game_state = GameState.RUNNING
            self.event_manager.emit(EventType.ON_MOVE_UNDONE, player=self.current_player)
            return True
        return False
    def redo(self) -> bool:
        if not self.can_redo():
            return False
        steps = (2 if (self.game_mode == GameMode.HUMAN_VS_AI and self.state_manager.redo_count >= 2 and not self.is_game_over()) else 1)
        redone = False
        for _ in range(steps):
            record = self.state_manager.redo()
            if record is None:
                break
            if self._apply_redo_record(record):
                self.move_count += 1
                redone = True
        if redone:
            self.event_manager.emit(EventType.ON_MOVE_REDONE, player=self.current_player)
            return True
        return False
    def _apply_undo_record(self, record: MoveRecord) -> bool:
        return True
    def _apply_redo_record(self, record: MoveRecord) -> bool:
        return True
    def get_board(self) -> Any:
        return self.board
    def get_current_player(self) -> int:
        return self.current_player
    def get_winner(self) -> int | None:
        return self.result.winner
    def get_result(self) -> GameResult:
        return self.result
    def get_game_state(self) -> int:
        return self.game_state
    def is_game_over(self) -> bool:
        return self.result.game_over
    def is_frozen(self) -> bool:
        return self.result.game_over
    def make_move(self, *args: Any, **kwargs: Any) -> bool:
        return False
    def get_legal_moves(self) -> list[Any]:
        return []
    def get_state(self) -> dict[str, Any]:
        return {"board": self.board.get_board_state() if hasattr(self.board, "get_board_state") else None,"current_player": self.current_player,"winner": self.result.winner,"game_state": self.game_state,"game_over": self.result.game_over,"draw": self.result.draw,"move_count": self.move_count,"legal_moves": self.get_legal_moves(),}
    def get_valid_moves_for_cell(self, *position: int) -> list[Any]:
        all_moves = self.get_legal_moves()
        if not position:
            return all_moves
        result: list[Any] = []
        for move in all_moves:
            if isinstance(move, (tuple, list)) and len(move) >= len(position):
                if tuple(move[: len(position)]) == position:
                    result.append(move)
        return result
    def get_hint(self) -> Any | None:
        if hasattr(self, "ai") and self.ai is not None:
            if hasattr(self.ai, "select_action"):
                return self.ai.select_action(self.get_state())
        return None
    def serialize(self) -> str:
        from engine.utils.serialization import serialize_game_state
        return serialize_game_state(self.get_state())
    def deserialize(self, data: str) -> bool:
        from engine.utils.serialization import deserialize_game_state
        state = deserialize_game_state(data)
        if not state:
            return False
        return True