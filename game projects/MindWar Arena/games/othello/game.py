# games/othello/game.py
from __future__ import annotations
from typing import Any
from engine.core.event_manager import get_event_manager
from engine.core.state_manager import MoveRecord, StateManager
from engine.game_base import GameBase
from engine.interfaces.game_result import GameResult
from engine.utils.constants import Difficulty, EventType
from games.othello.ai import OthelloAI
from games.othello.board import OthelloBoard
from games.othello.board_renderer import OthelloBoardRenderer
from games.othello.constants import (EMPTY,FIRST_PLAYER,GAME_DRAW,GAME_MODE_AI_VS_AI,GAME_MODE_HUMAN_VS_AI,GAME_MODE_HUMAN_VS_HUMAN,GAME_NOT_STARTED,GAME_OVER,GAME_RUNNING,PLAYER_BLACK,PLAYER_WHITE,)
from games.othello.human_player import HumanPlayer
from games.othello.overlay_renderer import OthelloOverlayRenderer
from games.othello.rules import OthelloRules
class OthelloGame(GameBase):
    def __init__(self,renderer: Any,game_mode: int = GAME_MODE_HUMAN_VS_HUMAN,difficulty: Difficulty = Difficulty.MEDIUM,) -> None:
        super().__init__(renderer, game_mode, difficulty)
        self.board = OthelloBoard()
        self.current_player = FIRST_PLAYER
        self.next_starting_player = FIRST_PLAYER
        self.result = GameResult()
        self.game_state = GAME_NOT_STARTED
        self.move_count = 0
        self.consecutive_passes = 0
        self.board_renderer = OthelloBoardRenderer()
        self.overlay_renderer = OthelloOverlayRenderer()
        self.human_player = HumanPlayer(self.board_renderer)
        self.ai = OthelloAI(player=PLAYER_WHITE, difficulty=difficulty)
        self.state_manager = StateManager(max_history=100)
        self.event_manager = get_event_manager()
    def set_difficulty(self, difficulty: Difficulty) -> None:
        self.difficulty = difficulty
        if isinstance(self.ai, OthelloAI):
            self.ai.set_difficulty(difficulty)
    def initialize(self) -> None:
        if self.game_mode in (GAME_MODE_HUMAN_VS_AI, GAME_MODE_AI_VS_AI):
            self.ai.initialize()
        self.reset()
    def reset(self) -> None:
        self.board.reset()
        self.current_player = self.choose_starting_player()
        self.next_starting_player = (PLAYER_WHITE if self.current_player == PLAYER_BLACK else PLAYER_BLACK)
        self.result.reset()
        self.game_state = GAME_RUNNING
        self.move_count = 0
        self.consecutive_passes = 0
        self.state_manager.clear()
        self.board_renderer.reset()
        self.overlay_renderer.reset()
        if self.game_mode in (GAME_MODE_HUMAN_VS_AI, GAME_MODE_AI_VS_AI):
            self.ai.reset()
            self.ai.set_player(PLAYER_WHITE)
            self.ai.initialize()
        self.event_manager.emit(EventType.ON_GAME_RESET)
    def shutdown(self) -> None:
        pass
    def update(self) -> None:
        if self.is_frozen():
            return
        self.update_current_player()
    def render(self) -> None:
        self.board_renderer.render(self.renderer, self.board, self.result)
        self.overlay_renderer.render(self.renderer, self.result, self.board)
    def make_move(self, *args: Any, **kwargs: Any) -> bool:
        if self.is_frozen():
            return False
        if len(args) == 1 and isinstance(args[0], (tuple, list)):
            row, column = args[0]
        elif len(args) == 2:
            row, column = args
        else:
            return False
        if not self.board.is_valid_position(row, column):
            return False
        if not OthelloRules.is_valid_move(self.board, row, column, self.current_player):
            return False
        flips = OthelloRules.get_flips(self.board, row, column, self.current_player)
        opponent = OthelloRules.get_opponent(self.current_player)
        captured_pieces = [(r, c, opponent) for (r, c) in flips]
        record = MoveRecord(move=(row, column),player=self.current_player,captured_pieces=captured_pieces,)
        if not OthelloRules.apply_move(self.board, row, column, self.current_player):
            return False
        self.state_manager.push(record)
        self.move_count += 1
        self.consecutive_passes = 0
        self.event_manager.emit(EventType.ON_MOVE_MADE,move=(row, column),player=self.current_player,flips_count=len(flips),move_count=self.move_count,)
        self.result = OthelloRules.evaluate_game(self.board)
        if self.result.game_over:
            self.game_state = GAME_DRAW if self.result.draw else GAME_OVER
            self.event_manager.emit(EventType.ON_GAME_OVER,winner=self.result.winner,draw=self.result.draw,)
            return True
        self.switch_player()
        self.event_manager.emit(EventType.ON_TURN_CHANGED, player=self.current_player)
        if not self.get_legal_moves():
            self.pass_turn()
        return True
    def pass_turn(self) -> bool:
        if self.is_frozen():
            return False
        if self.get_legal_moves():
            return False
        self.consecutive_passes += 1
        if self.consecutive_passes >= 2:
            self.result = OthelloRules.evaluate_game(self.board)
            self.game_state = GAME_DRAW if self.result.draw else GAME_OVER
            self.event_manager.emit(EventType.ON_GAME_OVER,winner=self.result.winner,draw=self.result.draw,)
            return True
        self.switch_player()
        self.event_manager.emit(EventType.ON_TURN_CHANGED, player=self.current_player)
        return True
    def can_undo(self) -> bool:
        return self.state_manager.can_undo()
    def undo(self) -> bool:
        if not self.can_undo():
            return False
        steps = (2 if (self.game_mode == GAME_MODE_HUMAN_VS_AI and self.state_manager.move_count >= 2 and not self.is_game_over()) else 1)
        for _ in range(steps):
            record = self.state_manager.undo()
            if record is None:
                break
            r, c = record.move
            self.board.set_cell(r, c, EMPTY)
            for fr, fc, prev_val in record.captured_pieces:
                self.board.set_cell(fr, fc, prev_val)
            self.current_player = record.player
            self.move_count = max(0, self.move_count - 1)
        self.result = OthelloRules.evaluate_game(self.board)
        self.game_state = GAME_RUNNING
        self.consecutive_passes = 0
        self.event_manager.emit(EventType.ON_MOVE_UNDONE, player=self.current_player)
        return True
    def can_redo(self) -> bool:
        return self.state_manager.can_redo()
    def redo(self) -> bool:
        if not self.can_redo():
            return False
        steps = (2 if (self.game_mode == GAME_MODE_HUMAN_VS_AI and self.state_manager.redo_count >= 2 and not self.is_game_over()) else 1)
        last_record = None
        for _ in range(steps):
            record = self.state_manager.redo()
            if record is None:
                break
            last_record = record
            r, c = record.move
            self.board.set_cell(r, c, record.player)
            for fr, fc, _ in record.captured_pieces:
                self.board.set_cell(fr, fc, record.player)
            self.move_count += 1
            self.result = OthelloRules.evaluate_game(self.board)
            if self.result.game_over:
                self.game_state = GAME_DRAW if self.result.draw else GAME_OVER
                break
            else:
                self.switch_player()
                if not self.get_legal_moves() and not self.is_game_over():
                    self.pass_turn()
        if last_record is not None:
            self.event_manager.emit(EventType.ON_MOVE_REDONE, move=last_record.move, player=last_record.player)
            return True
        return False
    def get_hint(self) -> tuple[int, int] | None:
        solver = OthelloAI(player=self.current_player, difficulty=Difficulty.IMPOSSIBLE)
        return solver.select_action(self.get_state())
    def get_legal_moves(self) -> list[tuple[int, int]]:
        return OthelloRules.get_legal_moves(self.board, self.current_player)
    def get_valid_moves_for_cell(self, *position: int) -> list[tuple[int, int]]:
        if not position:
            return self.get_legal_moves()
        r, c = position[0], position[1]
        if (r, c) in self.get_legal_moves():
            return [(r, c)]
        return []
    def switch_player(self) -> None:
        self.current_player = PLAYER_WHITE if self.current_player == PLAYER_BLACK else PLAYER_BLACK
    def choose_starting_player(self) -> int:
        player = self.next_starting_player
        self.next_starting_player = PLAYER_WHITE if player == PLAYER_BLACK else PLAYER_BLACK
        return player
    def get_current_controller(self) -> Any:
        if self.game_mode == GAME_MODE_HUMAN_VS_HUMAN:
            return self.human_player
        if self.game_mode == GAME_MODE_HUMAN_VS_AI:
            return self.human_player if self.current_player == PLAYER_BLACK else self.ai
        if self.game_mode == GAME_MODE_AI_VS_AI:
            return self.ai
        return self.human_player
    def update_current_player(self) -> None:
        controller = self.get_current_controller()
        if hasattr(controller, "set_player"):
            controller.set_player(self.current_player)
        move = controller.get_action(self)
        if move is None:
            return
        self.make_move(*move)
    def get_result(self) -> GameResult:
        return self.result
    def get_board(self) -> Any:
        return self.board
    def get_current_player(self) -> int:
        return self.current_player
    def get_winner(self) -> int | None:
        return self.result.winner
    def is_game_over(self) -> bool:
        return self.is_frozen()
    def is_frozen(self) -> bool:
        return self.result.game_over
    def get_state(self) -> dict[str, Any]:
        return {"board": self.board.get_board_state(),"current_player": self.current_player,"winner": self.result.winner,"game_state": self.game_state,"game_over": self.result.game_over,"draw": self.result.draw,"move_count": self.move_count,"legal_moves": self.get_legal_moves(),}