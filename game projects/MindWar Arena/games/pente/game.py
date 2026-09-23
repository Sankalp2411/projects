# games/pente/game.py
from __future__ import annotations
from typing import Any
from engine.core.event_manager import get_event_manager
from engine.core.state_manager import MoveRecord, StateManager
from engine.game_base import GameBase
from engine.interfaces.game_result import GameResult
from engine.utils.constants import Difficulty, EventType
from games.pente.ai import PenteAI
from games.pente.board import PenteBoard
from games.pente.board_renderer import BoardRenderer
from games.pente.constants import (FIRST_PLAYER,GAME_DRAW,GAME_MODE_AI_VS_AI,GAME_MODE_HUMAN_VS_AI,GAME_MODE_HUMAN_VS_HUMAN,GAME_NOT_STARTED,GAME_OVER,GAME_RUNNING,PLAYER_BLACK,PLAYER_WHITE,)
from games.pente.human_player import HumanPlayer
from games.pente.overlay_renderer import OverlayRenderer
from games.pente.rules import PenteRules
class PenteGame(GameBase):
    def __init__(self,renderer: Any,game_mode: int = GAME_MODE_HUMAN_VS_HUMAN,difficulty: Difficulty = Difficulty.MEDIUM,) -> None:
        super().__init__(renderer, game_mode, difficulty)
        self.board = PenteBoard()
        self.current_player = FIRST_PLAYER
        self.next_starting_player = FIRST_PLAYER
        self.result = GameResult()
        self.game_state = GAME_NOT_STARTED
        self.move_count = 0
        self.capture_counts = {PLAYER_BLACK: 0, PLAYER_WHITE: 0}
        self.board_renderer = BoardRenderer(renderer)
        self.overlay_renderer = OverlayRenderer(renderer)
        self.human_player = HumanPlayer(self.board_renderer)
        self.ai_player = PenteAI(player=PLAYER_WHITE, difficulty=difficulty)
        self.state_manager = StateManager(max_history=100)
        self.event_manager = get_event_manager()
        self._setup_controllers()
    def _setup_controllers(self) -> None:
        if self.game_mode == GAME_MODE_HUMAN_VS_HUMAN:
            self.player_black = self.human_player
            self.player_white = self.human_player
        elif self.game_mode == GAME_MODE_HUMAN_VS_AI:
            self.player_black = self.human_player
            self.player_white = self.ai_player
            self.ai_player.set_player(PLAYER_WHITE)
        elif self.game_mode == GAME_MODE_AI_VS_AI:
            self.player_black = PenteAI(player=PLAYER_BLACK, difficulty=self.difficulty)
            self.player_white = self.ai_player
            self.ai_player.set_player(PLAYER_WHITE)
        else:
            self.player_black = self.human_player
            self.player_white = self.human_player
    def set_difficulty(self, difficulty: Difficulty) -> None:
        self.difficulty = difficulty
        if isinstance(self.player_black, PenteAI):
            self.player_black.set_difficulty(difficulty)
        if isinstance(self.player_white, PenteAI):
            self.player_white.set_difficulty(difficulty)
    def initialize(self) -> None:
        if isinstance(self.player_black, PenteAI):
            self.player_black.initialize()
        if isinstance(self.player_white, PenteAI):
            self.player_white.initialize()
        self.reset()
    def reset(self) -> None:
        self.board.reset()
        self.current_player = self.choose_starting_player()
        self.result = GameResult()
        self.capture_counts = {PLAYER_BLACK: 0, PLAYER_WHITE: 0}
        self.game_state = GAME_RUNNING
        self.move_count = 0
        self.state_manager.clear()
        if isinstance(self.player_black, PenteAI):
            self.player_black.reset()
            self.player_black.initialize()
        if isinstance(self.player_white, PenteAI):
            self.player_white.reset()
            self.player_white.initialize()
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
        if not self.board.place_stone(row, column, self.current_player):
            return False
        self.move_count += 1
        captured_cells = PenteRules.find_captures(self.board, row, column, self.current_player)
        captured_count = PenteRules.apply_captures(self.board, captured_cells)
        captured_pairs = captured_count // 2
        self.capture_counts[self.current_player] += captured_pairs
        opponent = PenteRules.get_opponent(self.current_player)
        captured_pieces = [(r, c, opponent) for (r, c) in captured_cells]
        record = MoveRecord(move=(row, column),player=self.current_player,captured_pieces=captured_pieces,extra={"captured_pairs": captured_pairs},)
        self.state_manager.push(record)
        self.event_manager.emit(EventType.ON_MOVE_MADE,move=(row, column),player=self.current_player,captured_pairs=captured_pairs,move_count=self.move_count,)
        if captured_count > 0:
            self.event_manager.emit(EventType.ON_PIECE_CAPTURED,captured_positions=captured_cells,player=self.current_player,)
        self.result = PenteRules.evaluate_game(self.board, self.capture_counts)
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
            self.board.remove_stone(r, c)
            for cr, cc, piece_val in record.captured_pieces:
                self.board.place_stone(cr, cc, piece_val)
            pairs = record.extra.get("captured_pairs", 0)
            self.capture_counts[record.player] = max(0, self.capture_counts[record.player] - pairs)
            self.current_player = record.player
            self.move_count = max(0, self.move_count - 1)
        self.result = PenteRules.evaluate_game(self.board, self.capture_counts)
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
            self.board.place_stone(r, c, record.player)
            for cr, cc, _ in record.captured_pieces:
                self.board.remove_stone(cr, cc)
            pairs = record.extra.get("captured_pairs", 0)
            self.capture_counts[record.player] += pairs
            self.move_count += 1
            self.result = PenteRules.evaluate_game(self.board, self.capture_counts)
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
        solver = PenteAI(player=self.current_player, difficulty=Difficulty.IMPOSSIBLE)
        return solver.select_action(self.get_state())
    def get_legal_moves(self) -> list[tuple[int, int]]:
        return self.board.get_empty_positions()
    def get_valid_moves_for_cell(self, *position: int) -> list[tuple[int, int]]:
        if not position:
            return self.get_legal_moves()
        r, c = position[0], position[1]
        if self.board.is_valid_position(r, c) and self.board.is_cell_empty(r, c):
            return [(r, c)]
        return []
    def switch_player(self) -> None:
        self.current_player = PLAYER_WHITE if self.current_player == PLAYER_BLACK else PLAYER_BLACK
    def choose_starting_player(self) -> int:
        player = self.next_starting_player
        self.next_starting_player = PLAYER_WHITE if player == PLAYER_BLACK else PLAYER_BLACK
        return player
    def get_current_controller(self) -> Any:
        return self.player_black if self.current_player == PLAYER_BLACK else self.player_white
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
        return {"board": self.board.get_board_state(),"current_player": self.current_player,"winner": self.result.winner,"game_state": self.game_state,"game_over": self.result.game_over,"draw": self.result.draw,"move_count": self.move_count,"capture_counts": dict(self.capture_counts),"legal_moves": self.get_legal_moves(),}