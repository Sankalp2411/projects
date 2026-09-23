# games/nine_mens_morris/game.py
from __future__ import annotations
from typing import Any
from engine.core.event_manager import get_event_manager
from engine.core.state_manager import MoveRecord, StateManager
from engine.game_base import GameBase
from engine.interfaces.game_result import GameResult
from engine.utils.constants import Difficulty, EventType
from games.nine_mens_morris.ai import NineMensMorrisAI
from games.nine_mens_morris.board import NineMensMorrisBoard
from games.nine_mens_morris.board_renderer import BoardRenderer
from games.nine_mens_morris.constants import (FIRST_PLAYER,GAME_DRAW,GAME_MODE_AI_VS_AI,GAME_MODE_HUMAN_VS_AI,GAME_MODE_HUMAN_VS_HUMAN,GAME_NOT_STARTED,GAME_OVER,GAME_RUNNING,PHASE_FLYING,PHASE_MOVEMENT,PHASE_PLACEMENT,PIECES_PER_PLAYER,PLAYER_BLACK,PLAYER_WHITE,)
from games.nine_mens_morris.human_player import HumanPlayer
from games.nine_mens_morris.overlay_renderer import OverlayRenderer
from games.nine_mens_morris.rules import NineMensMorrisRules
class NineMensMorrisGame(GameBase):
    def __init__(self,renderer: Any | None = None,game_mode: int = GAME_MODE_HUMAN_VS_HUMAN,difficulty: Difficulty = Difficulty.MEDIUM,) -> None:
        super().__init__(renderer, game_mode, difficulty)
        self.board: NineMensMorrisBoard = NineMensMorrisBoard()
        self.current_player = FIRST_PLAYER
        self.next_starting_player = FIRST_PLAYER
        self.result = GameResult()
        self.game_state = GAME_NOT_STARTED
        self.move_count = 0
        self.pieces_placed = {PLAYER_BLACK: 0, PLAYER_WHITE: 0}
        self.capture_pending = False
        self.board_renderer = BoardRenderer(renderer)
        self.overlay_renderer = OverlayRenderer(renderer)
        self.human_player = HumanPlayer(self.board_renderer)
        self.ai_player = NineMensMorrisAI(player=PLAYER_WHITE, difficulty=difficulty)
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
            self.player_black = NineMensMorrisAI(player=PLAYER_BLACK, difficulty=self.difficulty)
            self.player_white = self.ai_player
            self.ai_player.set_player(PLAYER_WHITE)
        else:
            self.player_black = self.human_player
            self.player_white = self.human_player
    def set_difficulty(self, difficulty: Difficulty) -> None:
        self.difficulty = difficulty
        if isinstance(self.player_black, NineMensMorrisAI):
            self.player_black.set_difficulty(difficulty)
        if isinstance(self.player_white, NineMensMorrisAI):
            self.player_white.set_difficulty(difficulty)
    def initialize(self) -> None:
        if isinstance(self.player_black, NineMensMorrisAI):
            self.player_black.initialize()
        if isinstance(self.player_white, NineMensMorrisAI):
            self.player_white.initialize()
        self.reset()
    def reset(self) -> None:
        self.board.reset()
        self.choose_starting_player()
        self.result = GameResult()
        self.pieces_placed = {PLAYER_BLACK: 0, PLAYER_WHITE: 0}
        self.capture_pending = False
        self.game_state = GAME_RUNNING
        self.move_count = 0
        self.state_manager.clear()
        self.board_renderer.reset()
        self.overlay_renderer.reset()
        self.human_player.reset()
        if isinstance(self.player_black, NineMensMorrisAI):
            self.player_black.reset()
            self.player_black.initialize()
        if isinstance(self.player_white, NineMensMorrisAI):
            self.player_white.reset()
            self.player_white.initialize()
        self.event_manager.emit(EventType.ON_GAME_RESET)
    def shutdown(self) -> None:
        pass
    def update(self) -> None:
        if self.is_frozen():
            return
        if self.capture_pending:
            self.update_capture_controller()
            return
        self.update_current_player()
    def render(self) -> None:
        selected_position = self.human_player.selected_position
        self.board_renderer.render(self.board, self.result, selected_position)
        self.overlay_renderer.render(self.result)
        self.render_information()
    def render_information(self) -> None:
        phase_name = self.get_phase_name()
        self.renderer.draw_text(f"Phase: {phase_name}", (700, 80), size=28)
        self.renderer.draw_text(f"Black: {self.board.count_pieces(PLAYER_BLACK)}", (700, 125), size=26)
        self.renderer.draw_text(f"White: {self.board.count_pieces(PLAYER_WHITE)}", (700, 165), size=26)
        if self.capture_pending:
            self.renderer.draw_text("Select an opponent piece to remove", (700, 225), size=24)
        else:
            current_name = "Black" if self.current_player == PLAYER_BLACK else "White"
            self.renderer.draw_text(f"Turn: {current_name}", (700, 225), size=26)
    def make_move(self, *args: Any, **kwargs: Any) -> bool:
        if self.is_frozen():
            return False
        if not args:
            return False
        record = MoveRecord(move=args[0] if len(args) == 1 else tuple(args),player=self.current_player,previous_state={"board": list(self.board._board),"pieces_placed": dict(self.pieces_placed),"capture_pending": self.capture_pending,"game_state": self.game_state,},)
        applied = self._apply_raw_move(*args)
        if applied:
            self.state_manager.push(record)
            self.event_manager.emit(EventType.ON_MOVE_MADE,move=record.move,player=record.player,move_count=self.move_count,)
        return applied
    def _apply_raw_move(self, *args: Any) -> bool:
        applied = False
        if self.capture_pending:
            if len(args) == 1 and isinstance(args[0], int):
                applied = self.remove_opponent_piece(args[0])
            elif len(args) == 1 and isinstance(args[0], (tuple, list)):
                applied = self.remove_opponent_piece(args[0][0])
        else:
            phase = self.get_phase()
            if phase == PHASE_PLACEMENT:
                pos = (args[0][0] if (len(args) == 1 and isinstance(args[0], (tuple, list))) else args[0])
                applied = self.place_piece(pos)
            elif phase in (PHASE_MOVEMENT, PHASE_FLYING):
                if len(args) == 1 and isinstance(args[0], (tuple, list)) and len(args[0]) == 2:
                    applied = self.move_piece(args[0][0], args[0][1])
                elif len(args) == 2:
                    applied = self.move_piece(args[0], args[1])
        return applied
    def place_piece(self, position: int) -> bool:
        if not self.board.is_valid_position(position):
            return False
        if not self.board.is_position_empty(position):
            return False
        if self.pieces_placed[self.current_player] >= PIECES_PER_PLAYER:
            return False
        if not self.board.place_piece(position, self.current_player):
            return False
        self.pieces_placed[self.current_player] += 1
        self.move_count += 1
        if NineMensMorrisRules.is_mill(self.board, position, self.current_player):
            self.capture_pending = True
            removable = NineMensMorrisRules.get_removable_pieces(self.board, self.current_player)
            if not removable:
                self.capture_pending = False
                self.switch_player()
            return True
        self.switch_player()
        return True
    def move_piece(self, source: int, destination: int) -> bool:
        if not self.board.is_valid_position(source) or not self.board.is_valid_position(destination):
            return False
        if self.board.get_position(source) != self.current_player:
            return False
        if not self.board.is_position_empty(destination):
            return False
        legal_destinations = NineMensMorrisRules.get_legal_destinations(self.board, source, self.current_player)
        if destination not in legal_destinations:
            return False
        if not self.board.move_piece(source, destination, self.current_player):
            return False
        self.move_count += 1
        if NineMensMorrisRules.is_mill(self.board, destination, self.current_player):
            self.capture_pending = True
            removable = NineMensMorrisRules.get_removable_pieces(self.board, self.current_player)
            if not removable:
                self.capture_pending = False
                self.check_game_result()
                if not self.is_frozen():
                    self.switch_player()
            return True
        self.check_game_result()
        if self.is_frozen():
            return True
        self.switch_player()
        return True
    def remove_opponent_piece(self, position: int) -> bool:
        if not self.capture_pending:
            return False
        if not NineMensMorrisRules.can_remove_piece(self.board, position, self.current_player):
            return False
        if not self.board.remove_piece(position):
            return False
        self.capture_pending = False
        self.event_manager.emit(EventType.ON_PIECE_CAPTURED,captured_positions=[position],player=self.current_player,)
        self.check_game_result()
        if self.is_frozen():
            return True
        self.switch_player()
        return True
    def check_game_result(self) -> None:
        if self.get_phase() == PHASE_PLACEMENT:
            return
        opponent = NineMensMorrisRules.get_opponent(self.current_player)
        if opponent == 0:
            return
        if self.board.count_pieces(opponent) < 3:
            self.result = GameResult()
            self.result.winner = self.current_player
            self.result.game_over = True
            self.game_state = GAME_OVER
            self.event_manager.emit(EventType.ON_GAME_OVER, winner=self.current_player, draw=False)
            return
        if not NineMensMorrisRules.has_legal_move(self.board, opponent):
            self.result = GameResult()
            self.result.winner = self.current_player
            self.result.game_over = True
            self.game_state = GAME_OVER
            self.event_manager.emit(EventType.ON_GAME_OVER, winner=self.current_player, draw=False)
            return
        if self.board.is_board_full():
            self.result = GameResult()
            self.result.draw = True
            self.result.game_over = True
            self.game_state = GAME_DRAW
            self.event_manager.emit(EventType.ON_GAME_OVER, winner=None, draw=True)
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
            st = record.previous_state
            self.board._board = list(st["board"])
            self.pieces_placed = dict(st["pieces_placed"])
            self.capture_pending = st["capture_pending"]
            self.game_state = st.get("game_state", GAME_RUNNING)
            self.current_player = record.player
            self.move_count = max(0, self.move_count - 1)
        self.result = GameResult()
        self.game_state = GAME_RUNNING
        self.event_manager.emit(EventType.ON_MOVE_UNDONE, player=self.current_player)
        return True
    def can_redo(self) -> bool:
        return self.state_manager.can_redo()
    def redo(self) -> bool:
        if not self.can_redo():
            return False
        steps = (2 if (self.game_mode == GAME_MODE_HUMAN_VS_AI and self.state_manager.redo_count >= 2 and not self.is_game_over()) else 1)
        for _ in range(steps):
            record = self.state_manager.redo()
            if record is None:
                break
            move = record.move
            args = move if isinstance(move, tuple) else (move,)
            applied = self._apply_raw_move(*args)
            if not applied:
                self.state_manager.undo()
                return False
            self.event_manager.emit(EventType.ON_MOVE_REDONE,move=move,player=record.player,)
        return True
    def get_hint(self) -> Any | None:
        solver = NineMensMorrisAI(player=self.current_player, difficulty=Difficulty.IMPOSSIBLE)
        return solver.select_action(self.get_state())
    def switch_player(self) -> None:
        self.current_player = PLAYER_WHITE if self.current_player == PLAYER_BLACK else PLAYER_BLACK
        self.event_manager.emit(EventType.ON_TURN_CHANGED, player=self.current_player)
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
        if isinstance(move, tuple):
            self.make_move(*move)
        else:
            self.make_move(move)
    def update_capture_controller(self) -> None:
        controller = self.get_current_controller()
        move = controller.get_action(self)
        if move is None:
            return
        if isinstance(move, tuple):
            return
        self.make_move(move)
    def get_result(self) -> GameResult:
        return self.result
    def get_board(self) -> Any:
        return self.board
    def get_current_player(self) -> int:
        return self.current_player
    def get_phase(self) -> int:
        if (self.pieces_placed[PLAYER_BLACK] < PIECES_PER_PLAYER or self.pieces_placed[PLAYER_WHITE] < PIECES_PER_PLAYER):
            return PHASE_PLACEMENT
        if NineMensMorrisRules.can_fly(self.board, self.current_player):
            return PHASE_FLYING
        return PHASE_MOVEMENT
    def get_phase_name(self) -> str:
        phase = self.get_phase()
        if phase == PHASE_PLACEMENT:
            return "Placement"
        if phase == PHASE_MOVEMENT:
            return "Movement"
        if phase == PHASE_FLYING:
            return "Flying"
        return "Unknown"
    def is_capture_pending(self) -> bool:
        return self.capture_pending
    def get_piece_count(self, player: int) -> int:
        return self.board.count_pieces(player)
    def get_piece_counts(self) -> dict[int, int]:
        return {PLAYER_BLACK: self.board.count_pieces(PLAYER_BLACK),PLAYER_WHITE: self.board.count_pieces(PLAYER_WHITE),}
    def get_legal_moves(self) -> list[Any]:
        if self.capture_pending:
            return NineMensMorrisRules.get_removable_pieces(self.board, self.current_player)
        phase = self.get_phase()
        if phase == PHASE_PLACEMENT:
            return self.board.get_available_positions()
        return NineMensMorrisRules.get_legal_moves(self.board, self.current_player)
    def get_valid_moves_for_cell(self, *position: int) -> list[Any]:
        if not position:
            return self.get_legal_moves()
        pos = position[0]
        phase = self.get_phase()
        if phase == PHASE_PLACEMENT:
            return [pos] if self.board.is_position_empty(pos) else []
        moves = NineMensMorrisRules.get_legal_moves(self.board, self.current_player)
        return [m for m in moves if m[0] == pos]
    def get_state(self) -> dict[str, Any]:
        return {"board": self.board.get_board_state(),"current_player": self.current_player,"winner": self.result.winner,"game_state": self.game_state,"game_over": self.result.game_over,"draw": self.result.draw,"move_count": self.move_count,"phase": self.get_phase(),"pieces_placed": dict(self.pieces_placed),"capture_pending": self.capture_pending,"flying": NineMensMorrisRules.can_fly(self.board, self.current_player),"legal_moves": self.get_legal_moves(),}
    def is_game_over(self) -> bool:
        return self.is_frozen()
    def get_winner(self) -> int | None:
        return self.result.winner
    def is_frozen(self) -> bool:
        return self.result.game_over