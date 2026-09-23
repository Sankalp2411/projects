# games/tic_tac_toe/game.py
from __future__ import annotations
from typing import Any
from engine.core.state_manager import MoveRecord
from engine.game_base import GameBase
from engine.interfaces.game_result import GameResult
from engine.utils.constants import Difficulty, EventType
from games.tic_tac_toe.ai import TicTacToeAI
from games.tic_tac_toe.board import TicTacToeBoard
from games.tic_tac_toe.board_renderer import BoardRenderer
from games.tic_tac_toe.constants import (EMPTY,FIRST_PLAYER,GAME_DRAW,GAME_MODE_AI_VS_AI,GAME_MODE_HUMAN_VS_AI,GAME_MODE_HUMAN_VS_HUMAN,GAME_OVER,GAME_RUNNING,PLAYER_O,PLAYER_X,)
from games.tic_tac_toe.human_player import HumanPlayer
from games.tic_tac_toe.overlay_renderer import OverlayRenderer
from games.tic_tac_toe.rules import TicTacToeRules
class TicTacToeGame(GameBase):
    def __init__(self,renderer: Any,game_mode: int = GAME_MODE_HUMAN_VS_HUMAN,difficulty: Difficulty = Difficulty.MEDIUM,) -> None:
        super().__init__(renderer, game_mode, difficulty)
        self.board = TicTacToeBoard()
        self.current_player = FIRST_PLAYER
        self.next_starting_player = FIRST_PLAYER
        self.board_renderer = BoardRenderer(renderer)
        self.overlay_renderer = OverlayRenderer(renderer)
        self.human_player = HumanPlayer(self.board_renderer)
        self.ai_player = TicTacToeAI(player=PLAYER_O, difficulty=difficulty)
        self.ai = self.ai_player
        self._setup_controllers()
    def _setup_controllers(self) -> None:
        if self.game_mode == GAME_MODE_HUMAN_VS_HUMAN:
            self.player_x = self.human_player
            self.player_o = self.human_player
        elif self.game_mode == GAME_MODE_HUMAN_VS_AI:
            self.player_x = self.human_player
            self.player_o = self.ai_player
            self.ai_player.set_player(PLAYER_O)
        elif self.game_mode == GAME_MODE_AI_VS_AI:
            self.player_x = TicTacToeAI(player=PLAYER_X, difficulty=self.difficulty)
            self.player_o = self.ai_player
            self.ai_player.set_player(PLAYER_O)
        else:
            self.player_x = self.human_player
            self.player_o = self.human_player
    def set_difficulty(self, difficulty: Difficulty) -> None:
        self.difficulty = difficulty
        if isinstance(self.player_x, TicTacToeAI):
            self.player_x.set_difficulty(difficulty)
        if isinstance(self.player_o, TicTacToeAI):
            self.player_o.set_difficulty(difficulty)
    def initialize(self) -> None:
        if isinstance(self.player_x, TicTacToeAI):
            self.player_x.initialize()
        if isinstance(self.player_o, TicTacToeAI):
            self.player_o.initialize()
        self.reset()
    def reset(self) -> None:
        self.board.reset()
        self.choose_starting_player()
        self.result = GameResult()
        self.game_state = GAME_RUNNING
        self.move_count = 0
        self.state_manager.clear()
        if isinstance(self.player_x, TicTacToeAI):
            self.player_x.reset()
            self.player_x.initialize()
        if isinstance(self.player_o, TicTacToeAI):
            self.player_o.reset()
            self.player_o.initialize()
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
        if len(args) == 1 and isinstance(args[0], (tuple, list)):
            row, column = args[0]
        elif len(args) == 2:
            row, column = args
        else:
            return False
        if not self.board.is_valid_position(row, column):
            return False
        if not self.board.is_cell_empty(row, column):
            return False
        record = MoveRecord(move=(row, column),player=self.current_player,metadata={"prev_game_state": self.game_state},)
        self.board.set_cell(row, column, self.current_player)
        self.state_manager.push(record)
        self.move_count += 1
        self.event_manager.emit(EventType.ON_MOVE_MADE,move=(row, column),player=self.current_player,move_count=self.move_count,)
        self.result = TicTacToeRules.evaluate_game(self.board)
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
        steps = (2 if (self.game_mode == GAME_MODE_HUMAN_VS_AI and self.state_manager.move_count >= 2 and not self.is_game_over()) else 1)
        for _ in range(steps):
            record = self.state_manager.undo()
            if record is None:
                break
            r, c = record.move
            self.board.set_cell(r, c, EMPTY)
            self.current_player = record.player
            self.move_count = max(0, self.move_count - 1)
        self.result = TicTacToeRules.evaluate_game(self.board)
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
            r, c = record.move
            self.board.set_cell(r, c, record.player)
            self.move_count += 1
            self.result = TicTacToeRules.evaluate_game(self.board)
            if self.result.game_over:
                self.game_state = GAME_DRAW if self.result.draw else GAME_OVER
                break
            else:
                self.switch_player()
        if last_record is not None:
            self.event_manager.emit(EventType.ON_MOVE_REDONE, move=last_record.move, player=last_record.player)
            return True
        return False
    def get_hint(self) -> tuple[int, int] | None:
        solver = TicTacToeAI(player=self.current_player, difficulty=Difficulty.IMPOSSIBLE)
        return solver.select_action(self.get_state())
    def get_legal_moves(self) -> list[tuple[int, int]]:
        return TicTacToeRules.get_legal_moves(self.board)
    def get_valid_moves_for_cell(self, *position: int) -> list[tuple[int, int]]:
        if not position:
            return self.get_legal_moves()
        r, c = position[0], position[1]
        if self.board.is_valid_position(r, c) and self.board.is_cell_empty(r, c):
            return [(r, c)]
        return []
    def switch_player(self) -> None:
        self.current_player = PLAYER_O if self.current_player == PLAYER_X else PLAYER_X
    def choose_starting_player(self) -> None:
        self.current_player = self.next_starting_player
        self.next_starting_player = PLAYER_O if self.next_starting_player == PLAYER_X else PLAYER_X
    def get_current_controller(self) -> Any:
        return self.player_x if self.current_player == PLAYER_X else self.player_o
    def update_current_player(self) -> None:
        controller = self.get_current_controller()
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