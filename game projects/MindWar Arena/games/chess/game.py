# games/chess/game.py
from __future__ import annotations
from typing import Any
from engine.core.event_manager import get_event_manager
from engine.core.state_manager import MoveRecord, StateManager
from engine.game_base import GameBase
from engine.interfaces.game_result import GameResult
from engine.utils.constants import Difficulty, EventType
from games.chess.ai import ChessAI
from games.chess.board import ChessBoard
from games.chess.board_renderer import ChessBoardRenderer
from games.chess.constants import (BLACK_KING,BLACK_ROOK,EMPTY,FIRST_PLAYER,GAME_DRAW,GAME_MODE_AI_VS_AI,GAME_MODE_HUMAN_VS_AI,GAME_MODE_HUMAN_VS_HUMAN,GAME_NOT_STARTED,GAME_OVER,GAME_RUNNING,PLAYER_BLACK,PLAYER_WHITE,WHITE_KING,WHITE_ROOK,)
from games.chess.human_player import HumanPlayer
from games.chess.overlay_renderer import ChessOverlayRenderer
from games.chess.rules import ChessRules
class ChessGame(GameBase):
    def __init__(self,renderer: Any,game_mode: int = GAME_MODE_HUMAN_VS_HUMAN,difficulty: Difficulty = Difficulty.MEDIUM,) -> None:
        super().__init__(renderer, game_mode, difficulty)
        self.board = ChessBoard()
        self.board_renderer = ChessBoardRenderer(renderer)
        self.overlay_renderer = ChessOverlayRenderer(renderer)
        self.current_player = FIRST_PLAYER
        self.next_starting_player = FIRST_PLAYER
        self.result = GameResult()
        self.game_state = GAME_NOT_STARTED
        self.position_state = "NORMAL"
        self.move_count = 0
        self.half_move_clock = 0
        self.last_move = None
        self.castling_rights = {"white_kingside": True,"white_queenside": True,"black_kingside": True,"black_queenside": True,}
        self.en_passant_target: tuple[int, int] | None = None
        self._position_history: list[str] = []
        self.white_controller: Any = None
        self.black_controller: Any = None
        self._create_controllers()
        self.state_manager = StateManager(max_history=100)
        self.event_manager = get_event_manager()
    def set_difficulty(self, difficulty: Difficulty) -> None:
        self.difficulty = difficulty
        if isinstance(self.white_controller, ChessAI):
            self.white_controller.set_difficulty(difficulty)
        if isinstance(self.black_controller, ChessAI):
            self.black_controller.set_difficulty(difficulty)
    def initialize(self) -> None:
        self.reset()
    def reset(self) -> None:
        self.board.reset()
        self.current_player = self.choose_starting_player()
        self.result.reset()
        self.game_state = GAME_RUNNING
        self.position_state = "NORMAL"
        self.move_count = 0
        self.half_move_clock = 0
        self.last_move = None
        self.castling_rights = {"white_kingside": True,"white_queenside": True,"black_kingside": True,"black_queenside": True,}
        self.en_passant_target = None
        self._position_history = [self._compute_position_key()]
        self.state_manager.clear()
        self.board_renderer.reset()
        self.overlay_renderer.reset()
        self._reset_controllers()
        self.event_manager.emit(EventType.ON_GAME_RESET)
    def shutdown(self) -> None:
        pass
    def _create_controllers(self) -> None:
        if self.game_mode == GAME_MODE_HUMAN_VS_HUMAN:
            self.white_controller = HumanPlayer(self.board_renderer)
            self.black_controller = HumanPlayer(self.board_renderer)
        elif self.game_mode == GAME_MODE_HUMAN_VS_AI:
            self.white_controller = HumanPlayer(self.board_renderer)
            self.black_controller = ChessAI(PLAYER_BLACK, difficulty=self.difficulty)
        elif self.game_mode == GAME_MODE_AI_VS_AI:
            self.white_controller = ChessAI(PLAYER_WHITE, difficulty=self.difficulty)
            self.black_controller = ChessAI(PLAYER_BLACK, difficulty=self.difficulty)
        else:
            self.white_controller = HumanPlayer(self.board_renderer)
            self.black_controller = HumanPlayer(self.board_renderer)
    def _reset_controllers(self) -> None:
        if self.white_controller is not None and hasattr(self.white_controller, "reset"):
            self.white_controller.reset()
        if self.black_controller is not None and hasattr(self.black_controller, "reset"):
            self.black_controller.reset()
    def update(self) -> None:
        if self.is_frozen():
            return
        self.update_current_player()
    def render(self) -> None:
        if self.board_renderer is None:
            return
        check_pos = self._get_check_position()
        sel_pos = self._get_selected_position()
        self.board_renderer.render(board=self.board,legal_moves=self.get_legal_moves(),selected_position=sel_pos,last_move=self.last_move,check_position=check_pos,en_passant_target=self.en_passant_target,)
        self._render_overlay()
    def _render_overlay(self) -> None:
        if self.overlay_renderer is None:
            return
        if self.position_state == "CHECKMATE":
            self.overlay_renderer.draw_checkmate(winner=self.result.winner)
            return
        if self.position_state == "STALEMATE":
            self.overlay_renderer.draw_stalemate()
            return
        if self.result.draw:
            self.overlay_renderer.draw_draw()
            return
        if self.result.game_over:
            self.overlay_renderer.draw_game_over(winner=self.result.winner, draw=self.result.draw)
            return
        if self.position_state == "CHECK":
            self.overlay_renderer.draw_check()
    def make_move(self, *args: Any, **kwargs: Any) -> bool:
        if self.is_frozen():
            return False
        if not args:
            return False
        move = args[0] if len(args) == 1 else args
        if not isinstance(move, (tuple, list)) or len(move) not in (4, 5):
            return False
        move = tuple(move)
        if not ChessRules.is_valid_move(self.board, move, self.current_player, self.en_passant_target, self.castling_rights):
            return False
        from_row, from_column, to_row, to_column = move[:4]
        piece = self.board.get_cell(from_row, from_column)
        is_capture = ChessRules.is_capture_move(self.board, move, self.current_player, self.en_passant_target, self.castling_rights)
        board_snapshot = self.board.get_board_state()
        prev_castling = dict(self.castling_rights)
        prev_ep = self.en_passant_target
        prev_half_clock = self.half_move_clock
        prev_last_move = self.last_move
        record = MoveRecord(move=move,player=self.current_player,previous_state={"board": board_snapshot,"castling_rights": prev_castling,"en_passant_target": prev_ep,"half_move_clock": prev_half_clock,"last_move": prev_last_move,},)
        if is_capture or ChessRules.is_pawn(piece):
            self.half_move_clock = 0
        else:
            self.half_move_clock += 1
        if not ChessRules.apply_move(self.board, move, self.current_player, self.en_passant_target, self.castling_rights):
            return False
        self.state_manager.push(record)
        self.move_count += 1
        self.last_move = move
        self._update_castling_rights(piece, move)
        self._update_en_passant(piece, move)
        pos_key = self._compute_position_key()
        self._position_history.append(pos_key)
        self.event_manager.emit(EventType.ON_MOVE_MADE,move=move,player=self.current_player,is_capture=is_capture,move_count=self.move_count,)
        self.switch_player()
        self._evaluate_position()
        self.event_manager.emit(EventType.ON_TURN_CHANGED, player=self.current_player)
        return True
    def _compute_position_key(self) -> str:
        board_str = "".join(str(c) for row in self.board.get_board_state() for c in row)
        castling_str = "".join("1" if self.castling_rights[k] else "0" for k in sorted(self.castling_rights.keys()))
        ep_str = f"{self.en_passant_target}"
        return f"{board_str}:{self.current_player}:{castling_str}:{ep_str}"
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
            self.board.set_board_state(st["board"])
            self.castling_rights = dict(st["castling_rights"])
            self.en_passant_target = st["en_passant_target"]
            self.half_move_clock = st["half_move_clock"]
            self.last_move = st["last_move"]
            self.current_player = record.player
            self.move_count = max(0, self.move_count - 1)
            if self._position_history:
                self._position_history.pop()
        self._evaluate_position()
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
            piece = self.board.get_cell(move[0], move[1])
            is_capture = self.board.get_cell(move[2], move[3]) != EMPTY or (ChessRules.is_pawn(piece) and (move[2], move[3]) == self.en_passant_target)
            if is_capture or ChessRules.is_pawn(piece):
                self.half_move_clock = 0
            else:
                self.half_move_clock += 1
            if not ChessRules.apply_move(self.board, move, record.player, self.en_passant_target, self.castling_rights):
                self.state_manager.undo()
                return False
            self.move_count += 1
            self.last_move = move
            self._update_castling_rights(piece, move)
            self._update_en_passant(piece, move)
            pos_key = self._compute_position_key()
            self._position_history.append(pos_key)
            self.switch_player()
            self._evaluate_position()
            self.event_manager.emit(EventType.ON_MOVE_REDONE,move=move,player=record.player,)
        return True
    def get_hint(self) -> tuple[int, ...] | None:
        solver = ChessAI(player=self.current_player, difficulty=Difficulty.IMPOSSIBLE)
        return solver.select_action(self.get_state())
    def switch_player(self) -> None:
        self.current_player = PLAYER_BLACK if self.current_player == PLAYER_WHITE else PLAYER_WHITE
    def choose_starting_player(self) -> int:
        player = self.next_starting_player
        self.next_starting_player = PLAYER_BLACK if player == PLAYER_WHITE else PLAYER_WHITE
        return player
    def get_current_controller(self) -> Any:
        return (self.white_controller if self.current_player == PLAYER_WHITE else self.black_controller)
    def update_current_player(self) -> None:
        controller = self.get_current_controller()
        if controller is None:
            return
        action = controller.get_action(self)
        if action is None:
            return
        self.make_move(action)
    def _update_castling_rights(self, piece: int, move: tuple[int, ...]) -> None:
        from_row, from_column, to_row, to_column = move[:4]
        if piece == WHITE_KING:
            self.castling_rights["white_kingside"] = False
            self.castling_rights["white_queenside"] = False
        elif piece == BLACK_KING:
            self.castling_rights["black_kingside"] = False
            self.castling_rights["black_queenside"] = False
        if piece == WHITE_ROOK:
            if from_row == 7 and from_column == 0:
                self.castling_rights["white_queenside"] = False
            elif from_row == 7 and from_column == 7:
                self.castling_rights["white_kingside"] = False
        elif piece == BLACK_ROOK:
            if from_row == 0 and from_column == 0:
                self.castling_rights["black_queenside"] = False
            elif from_row == 0 and from_column == 7:
                self.castling_rights["black_kingside"] = False
        if to_row == 7 and to_column == 0:
            self.castling_rights["white_queenside"] = False
        elif to_row == 7 and to_column == 7:
            self.castling_rights["white_kingside"] = False
        elif to_row == 0 and to_column == 0:
            self.castling_rights["black_queenside"] = False
        elif to_row == 0 and to_column == 7:
            self.castling_rights["black_kingside"] = False
    def _update_en_passant(self, piece: int, move: tuple[int, ...]) -> None:
        self.en_passant_target = None
        if not ChessRules.is_pawn(piece):
            return
        from_row, from_column, to_row, to_column = move[:4]
        if abs(to_row - from_row) == 2:
            self.en_passant_target = ((from_row + to_row) // 2, from_column)
    def _evaluate_position(self) -> None:
        self.result.reset()
        self.position_state = "NORMAL"
        white_king = self.board.find_king(PLAYER_WHITE)
        black_king = self.board.find_king(PLAYER_BLACK)
        if white_king is None:
            self.result.game_over = True
            self.result.winner = PLAYER_BLACK
            self.game_state = GAME_OVER
            self.position_state = "CHECKMATE"
            self.event_manager.emit(EventType.ON_CHECKMATE, winner=PLAYER_BLACK)
            return
        if black_king is None:
            self.result.game_over = True
            self.result.winner = PLAYER_WHITE
            self.game_state = GAME_OVER
            self.position_state = "CHECKMATE"
            self.event_manager.emit(EventType.ON_CHECKMATE, winner=PLAYER_WHITE)
            return
        if ChessRules.is_insufficient_material(self.board):
            self.set_draw()
            self.event_manager.emit(EventType.ON_GAME_OVER, winner=None, draw=True, reason="insufficient_material")
            return
        legal_moves = ChessRules.get_legal_moves(self.board, self.current_player, self.en_passant_target, self.castling_rights)
        current_in_check = ChessRules.is_in_check(self.board, self.current_player)
        if not legal_moves:
            if current_in_check:
                self.result.winner = (PLAYER_BLACK if self.current_player == PLAYER_WHITE else PLAYER_WHITE)
                self.result.game_over = True
                self.game_state = GAME_OVER
                self.position_state = "CHECKMATE"
                self.event_manager.emit(EventType.ON_CHECKMATE, winner=self.result.winner)
            else:
                self.result.winner = None
                self.result.game_over = True
                self.result.draw = True
                self.game_state = GAME_DRAW
                self.position_state = "STALEMATE"
                self.event_manager.emit(EventType.ON_GAME_OVER, winner=None, draw=True)
            return
        if self.half_move_clock >= 100:
            self.set_draw()
            self.event_manager.emit(EventType.ON_GAME_OVER, winner=None, draw=True, reason="50_move_rule")
            return
        current_key = self._compute_position_key()
        if self._position_history.count(current_key) >= 3:
            self.set_draw()
            self.event_manager.emit(EventType.ON_GAME_OVER, winner=None, draw=True, reason="threefold_repetition")
            return
        self.result.game_over = False
        self.result.draw = False
        self.result.winner = None
        self.game_state = GAME_RUNNING
        if current_in_check:
            self.position_state = "CHECK"
        else:
            self.position_state = "NORMAL"
    def get_legal_moves(self) -> list[tuple[int, ...]]:
        return ChessRules.get_legal_moves(self.board, self.current_player, self.en_passant_target, self.castling_rights)
    def get_valid_moves_for_cell(self, *position: int) -> list[tuple[int, ...]]:
        if not position or len(position) < 2:
            return self.get_legal_moves()
        r, c = position[0], position[1]
        all_moves = self.get_legal_moves()
        return [m for m in all_moves if m[0] == r and m[1] == c]
    def _get_check_position(self) -> tuple[int, int] | None:
        if self.position_state in ("CHECK", "CHECKMATE"):
            return self.board.find_king(self.current_player)
        return None
    def _get_selected_position(self) -> tuple[int, int] | None:
        controller = self.get_current_controller()
        if hasattr(controller, "get_selected_position"):
            return controller.get_selected_position()
        return None
    def get_state(self) -> dict[str, Any]:
        return {"board": self.board.get_board_state(),"current_player": self.current_player,"winner": self.result.winner,"game_state": self.game_state,"position_state": self.position_state,"game_over": self.result.game_over,"draw": self.result.draw,"move_count": self.move_count,"half_move_clock": self.half_move_clock,"last_move": self.last_move,"castling_rights": dict(self.castling_rights),"en_passant_target": self.en_passant_target,"legal_moves": self.get_legal_moves(),}
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
    def get_position_state(self) -> str:
        return self.position_state
    def get_move_count(self) -> int:
        return self.move_count
    def get_half_move_clock(self) -> int:
        return self.half_move_clock
    def get_last_move(self) -> tuple[int, ...] | None:
        return self.last_move
    def get_castling_rights(self) -> dict[str, bool]:
        return dict(self.castling_rights)
    def get_en_passant_target(self) -> tuple[int, int] | None:
        return self.en_passant_target
    def is_game_over(self) -> bool:
        return self.result.game_over
    def is_frozen(self) -> bool:
        return self.result.game_over
    def is_draw(self) -> bool:
        return self.result.draw
    def set_draw(self) -> None:
        self.result.reset()
        self.result.game_over = True
        self.result.draw = True
        self.result.winner = None
        self.game_state = GAME_DRAW
        self.position_state = "NORMAL"