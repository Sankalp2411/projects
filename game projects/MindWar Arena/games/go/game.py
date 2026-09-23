# games/go/game.py
from __future__ import annotations
from typing import Any
from engine.core.event_manager import get_event_manager
from engine.core.state_manager import MoveRecord, StateManager
from engine.game_base import GameBase
from engine.interfaces.game_result import GameResult
from engine.utils.constants import Difficulty, EventType
from games.go.ai import GoAI
from games.go.board import GoBoard
from games.go.board_renderer import GoBoardRenderer
from games.go.constants import (ACTION_PASS,FIRST_PLAYER,GAME_DRAW,GAME_MODE_AI_VS_AI,GAME_MODE_HUMAN_VS_AI,GAME_MODE_HUMAN_VS_HUMAN,GAME_NOT_STARTED,GAME_OVER,GAME_RUNNING,PLAYER_BLACK,PLAYER_WHITE,)
from games.go.human_player import HumanPlayer
from games.go.overlay_renderer import GoOverlayRenderer
from games.go.rules import GoRules
class GoGame(GameBase):
    def __init__(self,renderer: Any | None = None,game_mode: int = GAME_MODE_HUMAN_VS_HUMAN,difficulty: Difficulty = Difficulty.MEDIUM,) -> None:
        super().__init__(renderer, game_mode, difficulty)
        self.board = GoBoard()
        self.board_renderer = GoBoardRenderer(renderer)
        self.overlay_renderer = GoOverlayRenderer(renderer)
        self.current_player = FIRST_PLAYER
        self.next_starting_player = FIRST_PLAYER
        self.result = GameResult()
        self.game_state = GAME_NOT_STARTED
        self.move_count = 0
        self.consecutive_passes = 0
        self.last_move = None
        self.ko_position = None
        self.previous_board = None
        self.black_controller = None
        self.white_controller = None
        self.state_manager = StateManager(max_history=200)
        self.event_manager = get_event_manager()
        self._create_controllers()
    def initialize(self) -> None:
        self.reset()
    def reset(self) -> None:
        self.board.reset()
        self.current_player = self.choose_starting_player()
        self.result.reset()
        self.game_state = GAME_RUNNING
        self.move_count = 0
        self.consecutive_passes = 0
        self.last_move = None
        self.ko_position = None
        self.previous_board = None
        self.board_renderer.reset()
        self.overlay_renderer.reset()
        self.state_manager.clear()
        self._reset_controllers()
    def shutdown(self) -> None:
        pass
    def _create_controllers(self) -> None:
        if self.game_mode == GAME_MODE_HUMAN_VS_HUMAN:
            self.black_controller = HumanPlayer(self.board_renderer)
            self.white_controller = HumanPlayer(self.board_renderer)
        elif self.game_mode == GAME_MODE_HUMAN_VS_AI:
            self.black_controller = HumanPlayer(self.board_renderer)
            self.white_controller = GoAI(PLAYER_WHITE, difficulty=self.difficulty)
        elif self.game_mode == GAME_MODE_AI_VS_AI:
            self.black_controller = GoAI(PLAYER_BLACK, difficulty=self.difficulty)
            self.white_controller = GoAI(PLAYER_WHITE, difficulty=self.difficulty)
        else:
            raise ValueError(f"Invalid Go game mode: {self.game_mode}")
    def _reset_controllers(self) -> None:
        if self.black_controller is not None:
            if hasattr(self.black_controller, "reset"):
                self.black_controller.reset()
            if hasattr(self.black_controller, "initialize"):
                self.black_controller.initialize()
            if hasattr(self.black_controller, "set_player"):
                self.black_controller.set_player(PLAYER_BLACK)
        if self.white_controller is not None:
            if hasattr(self.white_controller, "reset"):
                self.white_controller.reset()
            if hasattr(self.white_controller, "initialize"):
                self.white_controller.initialize()
            if hasattr(self.white_controller, "set_player"):
                self.white_controller.set_player(PLAYER_WHITE)
    def update(self) -> None:
        if self.is_frozen():
            return
        self.update_current_player()
    def render(self) -> None:
        if self.board_renderer is None:
            return
        self.board_renderer.render(board=self.board,legal_moves=self.get_legal_moves(),last_move=self.last_move,ko_position=self.ko_position,)
        self.overlay_renderer.render(result=self.result,board=self.board,consecutive_passes=self.consecutive_passes,)
    def _snapshot_state(self) -> dict[str, Any]:
        return {"board": self.board.get_board_state(),"previous_board": self.previous_board.get_board_state() if self.previous_board else None,"current_player": self.current_player,"consecutive_passes": self.consecutive_passes,"move_count": self.move_count,"last_move": self.last_move,"ko_position": self.ko_position,"game_state": self.game_state,"game_over": self.result.game_over,"winner": self.result.winner,"draw": self.result.draw,}
    def _restore_snapshot(self, snap: dict[str, Any]) -> None:
        self.board.set_board_state(snap["board"])
        if snap["previous_board"] is not None:
            self.previous_board = GoBoard()
            self.previous_board.set_board_state(snap["previous_board"])
        else:
            self.previous_board = None
        self.current_player = snap["current_player"]
        self.consecutive_passes = snap["consecutive_passes"]
        self.move_count = snap["move_count"]
        self.last_move = snap["last_move"]
        self.ko_position = snap["ko_position"]
        self.game_state = snap["game_state"]
        self.result.game_over = snap["game_over"]
        self.result.winner = snap["winner"]
        self.result.draw = snap["draw"]
    def make_move(self, *args: Any, **kwargs: Any) -> bool:
        if len(args) == 2:
            row, column = args[0], args[1]
        elif len(args) == 1 and isinstance(args[0], (tuple, list)) and len(args[0]) == 2:
            row, column = args[0][0], args[0][1]
        else:
            return False
        if self.is_frozen():
            return False
        if not self.board.is_valid_position(row, column):
            return False
        if not GoRules.is_valid_move(self.board, row, column, self.current_player, self.ko_position):
            return False
        before_state = self._snapshot_state()
        old_board = self.board.copy()
        if not GoRules.apply_move(self.board, row, column, self.current_player, self.ko_position):
            return False
        self.previous_board = old_board
        self.move_count += 1
        self.consecutive_passes = 0
        self.last_move = (row, column)
        self._update_ko_position()
        moving_player = self.current_player
        self._switch_player()
        after_state = self._snapshot_state()
        self.state_manager.record_move(
            MoveRecord(player=moving_player,move=(row, column),before_state=before_state,after_state=after_state,))
        self.event_manager.emit(EventType.ON_MOVE_MADE, move=(row, column), player=moving_player)
        return True
    def pass_turn(self) -> bool:
        if self.is_frozen():
            return False
        before_state = self._snapshot_state()
        self.previous_board = self.board.copy()
        self.last_move = None
        self.ko_position = None
        self.consecutive_passes += 1
        self.move_count += 1
        passing_player = self.current_player
        if self.consecutive_passes >= 2:
            self._finish_game()
        else:
            self._switch_player()
        after_state = self._snapshot_state()
        self.state_manager.record_move(
            MoveRecord(player=passing_player,move=ACTION_PASS,before_state=before_state,after_state=after_state,))
        self.event_manager.emit(EventType.ON_MOVE_MADE, move=ACTION_PASS, player=passing_player)
        return True
    def can_undo(self) -> bool:
        return self.state_manager.can_undo()
    def undo(self) -> bool:
        if not self.can_undo():
            return False
        steps = (2 if (self.game_mode == GAME_MODE_HUMAN_VS_AI and self.state_manager.move_count >= 2 and not self.is_game_over()) else 1)
        record = None
        for _ in range(steps):
            rec = self.state_manager.undo()
            if rec is not None:
                record = rec
        if record is None:
            return False
        self._restore_snapshot(record.before_state)
        self.event_manager.emit(EventType.ON_UNDO)
        return True
    def can_redo(self) -> bool:
        return self.state_manager.can_redo()
    def redo(self) -> bool:
        if not self.can_redo():
            return False
        steps = (2 if (self.game_mode == GAME_MODE_HUMAN_VS_AI and self.state_manager.redo_count >= 2 and not self.is_game_over()) else 1)
        record = None
        for _ in range(steps):
            rec = self.state_manager.redo()
            if rec is not None:
                record = rec
        if record is None:
            return False
        self._restore_snapshot(record.after_state)
        self.event_manager.emit(EventType.ON_REDO)
        return True
    def get_hint(self) -> tuple[int, int] | None:
        hint_ai = GoAI(self.current_player, difficulty=Difficulty.IMPOSSIBLE)
        hint_ai.initialize()
        act = hint_ai.select_action(self.get_state())
        if act != ACTION_PASS and isinstance(act, tuple):
            return act
        return None
    def _finish_game(self) -> None:
        self.result = GoRules.evaluate_game(self.board)
        scores = GoRules.get_scores(self.board)
        self.result.scores = scores
        if self.result.draw:
            self.game_state = GAME_DRAW
        else:
            self.game_state = GAME_OVER
        self.event_manager.emit(EventType.ON_GAME_OVER, winner=self.result.winner, draw=self.result.draw)
    def _update_ko_position(self) -> None:
        self.ko_position = None
        if self.previous_board is None:
            return
        current_state = self.board.get_board_state()
        previous_state = self.previous_board.get_board_state()
        differences = []
        for row in range(len(current_state)):
            for column in range(len(current_state[row])):
                if current_state[row][column] != previous_state[row][column]:
                    differences.append((row, column))
        if len(differences) != 1:
            return
        row, column = differences[0]
        if current_state[row][column] == self.current_player:
            self.ko_position = (row, column)
    def switch_player(self) -> None:
        self._switch_player()
    def _switch_player(self) -> None:
        if self.current_player == PLAYER_BLACK:
            self.current_player = PLAYER_WHITE
        else:
            self.current_player = PLAYER_BLACK
    def choose_starting_player(self) -> int:
        player = self.next_starting_player
        if player == PLAYER_BLACK:
            self.next_starting_player = PLAYER_WHITE
        else:
            self.next_starting_player = PLAYER_BLACK
        return player
    def get_current_controller(self) -> Any:
        if self.current_player == PLAYER_BLACK:
            return self.black_controller
        if self.current_player == PLAYER_WHITE:
            return self.white_controller
        return None
    def update_current_player(self) -> None:
        controller = self.get_current_controller()
        if controller is None:
            return
        action = controller.get_action(self)
        if action is None:
            return
        if action == ACTION_PASS:
            self.pass_turn()
            return
        if not isinstance(action, tuple) or len(action) != 2:
            return
        row, column = action
        self.make_move(row, column)
    def get_state(self) -> dict[str, Any]:
        previous_board_state = None
        if self.previous_board is not None:
            previous_board_state = self.previous_board.get_board_state()
        scores = GoRules.get_scores(self.board)
        return {"board": self.board.get_board_state(),"previous_board": previous_board_state,"current_player": self.current_player,"winner": self.result.winner,"game_state": self.game_state,"game_over": self.result.game_over,"draw": self.result.draw,"move_count": self.move_count,"consecutive_passes": self.consecutive_passes,"last_move": self.last_move,"ko_position": self.ko_position,"black_count": self.board.count_stones(PLAYER_BLACK),"white_count": self.board.count_stones(PLAYER_WHITE),"black_score": scores[PLAYER_BLACK],"white_score": scores[PLAYER_WHITE],"legal_moves": self.get_legal_moves(),}
    def get_board(self) -> GoBoard:
        return self.board
    def get_current_player(self) -> int:
        return self.current_player
    def get_winner(self) -> int | None:
        return self.result.winner
    def get_result(self) -> GameResult:
        return self.result
    def get_game_state(self) -> int:
        return self.game_state
    def get_legal_moves(self) -> list[tuple[int, int]]:
        return GoRules.get_legal_moves(self.board, self.current_player, self.ko_position)
    def get_black_count(self) -> int:
        return self.board.count_stones(PLAYER_BLACK)
    def get_white_count(self) -> int:
        return self.board.count_stones(PLAYER_WHITE)
    def get_black_score(self) -> float:
        return GoRules.calculate_score(self.board, PLAYER_BLACK)
    def get_white_score(self) -> float:
        return GoRules.calculate_score(self.board, PLAYER_WHITE)
    def get_last_move(self) -> tuple[int, int] | None:
        return self.last_move
    def get_ko_position(self) -> tuple[int, int] | None:
        return self.ko_position
    def get_move_count(self) -> int:
        return self.move_count
    def get_consecutive_passes(self) -> int:
        return self.consecutive_passes
    def is_game_over(self) -> bool:
        return self.result.game_over
    def is_frozen(self) -> bool:
        return self.result.game_over
    def is_draw(self) -> bool:
        return self.result.draw