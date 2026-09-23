# games/connect4/game.py
from __future__ import annotations
from typing import Any
from engine.core.state_manager import MoveRecord
from engine.game_base import GameBase
from engine.interfaces.game_result import GameResult
from engine.utils.constants import Difficulty, EventType
from games.connect4.ai import Connect4AI
from games.connect4.board import Connect4Board
from games.connect4.board_renderer import BoardRenderer
from games.connect4.constants import (EMPTY,FIRST_PLAYER,GAME_DRAW,GAME_MODE_AI_VS_AI,GAME_MODE_HUMAN_VS_AI,GAME_MODE_HUMAN_VS_HUMAN,GAME_OVER,GAME_RUNNING,PLAYER_RED,PLAYER_YELLOW,)
from games.connect4.human_player import HumanPlayer
from games.connect4.overlay_renderer import OverlayRenderer
from games.connect4.rules import Connect4Rules
class Connect4Game(GameBase):
    def __init__(self,renderer: Any,game_mode: int = GAME_MODE_HUMAN_VS_HUMAN,difficulty: Difficulty = Difficulty.MEDIUM,) -> None:
        super().__init__(renderer, game_mode, difficulty)
        self.board = Connect4Board()
        self.current_player = FIRST_PLAYER
        self.next_starting_player = FIRST_PLAYER
        self.board_renderer = BoardRenderer(renderer)
        self.overlay_renderer = OverlayRenderer(renderer)
        self.human_player = HumanPlayer(self.board_renderer)
        self.ai_player = Connect4AI(player=PLAYER_YELLOW, difficulty=difficulty)
        self.ai = self.ai_player
        self._setup_controllers()
    def _setup_controllers(self) -> None:
        if self.game_mode == GAME_MODE_HUMAN_VS_HUMAN:
            self.player_red = self.human_player
            self.player_yellow = self.human_player
        elif self.game_mode == GAME_MODE_HUMAN_VS_AI:
            self.player_red = self.human_player
            self.player_yellow = self.ai_player
            self.ai_player.set_player(PLAYER_YELLOW)
        elif self.game_mode == GAME_MODE_AI_VS_AI:
            self.player_red = Connect4AI(player=PLAYER_RED, difficulty=self.difficulty)
            self.player_yellow = self.ai_player
            self.ai_player.set_player(PLAYER_YELLOW)
        else:
            self.player_red = self.human_player
            self.player_yellow = self.human_player
    def set_difficulty(self, difficulty: Difficulty) -> None:
        self.difficulty = difficulty
        if isinstance(self.player_red, Connect4AI):
            self.player_red.set_difficulty(difficulty)
        if isinstance(self.player_yellow, Connect4AI):
            self.player_yellow.set_difficulty(difficulty)
    def initialize(self) -> None:
        if isinstance(self.player_red, Connect4AI):
            self.player_red.initialize()
        if isinstance(self.player_yellow, Connect4AI):
            self.player_yellow.initialize()
        self.reset()
    def reset(self) -> None:
        self.board.reset()
        self.choose_starting_player()
        self.result = GameResult()
        self.game_state = GAME_RUNNING
        self.move_count = 0
        self.state_manager.clear()
        if isinstance(self.player_red, Connect4AI):
            self.player_red.reset()
            self.player_red.initialize()
        if isinstance(self.player_yellow, Connect4AI):
            self.player_yellow.reset()
            self.player_yellow.initialize()
        self.board_renderer.reset()
        self.overlay_renderer.reset()
        self.event_manager.emit(EventType.ON_GAME_RESET)
    def shutdown(self) -> None:
        pass
    def update(self) -> None:
        if self.is_frozen():
            return
        self.update_current_player()
    def render(self) -> None:
        self.board_renderer.render(self.board, self.result)
        self.overlay_renderer.render(self.result)
    def make_move(self, *args: Any, **kwargs: Any) -> bool:
        if self.is_frozen():
            return False
        if not args:
            return False
        column = args[0]
        if isinstance(column, (tuple, list)):
            column = column[0]
        if not isinstance(column, int):
            return False
        if self.board.is_column_full(column):
            return False
        row = self.board.drop_piece(column, self.current_player)
        if row is None:
            return False
        record = MoveRecord(move=column,player=self.current_player,extra={"row": row, "column": column},)
        self.state_manager.push(record)
        self.move_count += 1
        self.event_manager.emit(EventType.ON_MOVE_MADE,move=column,row=row,player=self.current_player,move_count=self.move_count,)
        self.result = Connect4Rules.evaluate_game(self.board)
        if self.result.game_over:
            if self.result.draw:
                self.game_state = GAME_DRAW
                self.event_manager.emit(EventType.ON_GAME_OVER, winner=None, draw=True)
            else:
                self.game_state = GAME_OVER
                self.event_manager.emit(EventType.ON_GAME_OVER, winner=self.result.winner, draw=False)
            return True
        self.switch_player()
        self.event_manager.emit(EventType.ON_TURN_CHANGED, player=self.current_player)
        return True
    def can_undo(self) -> bool:
        return self.state_manager.can_undo()
    def undo(self) -> bool:
        if not self.can_undo():
            return False
        steps = (
            2
            if (self.game_mode == GAME_MODE_HUMAN_VS_AI and self.state_manager.move_count >= 2 and not self.is_game_over()) else 1)
        for _ in range(steps):
            record = self.state_manager.undo()
            if record is None:
                break
            r = record.extra.get("row")
            c = record.extra.get("column", record.move)
            if r is not None:
                self.board.set_cell(r, c, EMPTY)
            self.current_player = record.player
            self.move_count = max(0, self.move_count - 1)
        self.result = Connect4Rules.evaluate_game(self.board)
        self.game_state = GAME_RUNNING
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
            column = record.move
            row = self.board.drop_piece(column, record.player)
            if row is None:
                break
            record.extra["row"] = row
            self.move_count += 1
            self.result = Connect4Rules.evaluate_game(self.board)
            if self.result.game_over:
                self.game_state = GAME_DRAW if self.result.draw else GAME_OVER
                break
            else:
                self.switch_player()
        if last_record is not None:
            self.event_manager.emit(EventType.ON_MOVE_REDONE, move=last_record.move, player=last_record.player)
            return True
        return False
    def get_hint(self) -> int | None:
        solver = Connect4AI(player=self.current_player, difficulty=Difficulty.IMPOSSIBLE)
        return solver.select_action(self.get_state())
    def get_legal_moves(self) -> list[int]:
        return self.board.get_available_columns()
    def get_valid_moves_for_cell(self, *position: int) -> list[int]:
        if not position:
            return self.get_legal_moves()
        col = position[1] if len(position) > 1 else position[0]
        if not self.board.is_column_full(col):
            return [col]
        return []
    def switch_player(self) -> None:
        self.current_player = PLAYER_YELLOW if self.current_player == PLAYER_RED else PLAYER_RED
    def choose_starting_player(self) -> None:
        self.current_player = self.next_starting_player
        self.next_starting_player = (PLAYER_YELLOW if self.next_starting_player == PLAYER_RED else PLAYER_RED)
    def get_current_controller(self) -> Any:
        return self.player_red if self.current_player == PLAYER_RED else self.player_yellow
    def update_current_player(self) -> None:
        controller = self.get_current_controller()
        move = controller.get_action(self)
        if move is None:
            return
        self.make_move(move)
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