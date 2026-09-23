# games/checkers/game.py
from __future__ import annotations
from typing import Any
from engine.core.state_manager import MoveRecord
from engine.game_base import GameBase
from engine.interfaces.game_result import GameResult
from engine.utils.constants import Difficulty, EventType
from games.checkers.ai import CheckersAI
from games.checkers.board import CheckersBoard
from games.checkers.board_renderer import CheckersBoardRenderer
from games.checkers.constants import (EMPTY,FIRST_PLAYER,GAME_DRAW,GAME_MODE_AI_VS_AI,GAME_MODE_HUMAN_VS_AI,GAME_MODE_HUMAN_VS_HUMAN,GAME_OVER,GAME_RUNNING,PLAYER_BLACK,PLAYER_WHITE,)
from games.checkers.human_player import HumanPlayer
from games.checkers.overlay_renderer import CheckersOverlayRenderer
from games.checkers.rules import CheckersRules
class CheckersGame(GameBase):
    def __init__(self,renderer: Any,game_mode: int = GAME_MODE_HUMAN_VS_HUMAN,difficulty: Difficulty = Difficulty.MEDIUM,) -> None:
        super().__init__(renderer, game_mode, difficulty)
        self.board = CheckersBoard()
        self.current_player = FIRST_PLAYER
        self.next_starting_player = FIRST_PLAYER
        self.in_multi_capture = False
        self.active_capture_piece = None
        self.half_move_clock = 0
        self.board_renderer = CheckersBoardRenderer(renderer)
        self.overlay_renderer = CheckersOverlayRenderer(renderer)
        self.human_player = HumanPlayer(self.board_renderer)
        self.ai = CheckersAI(player=PLAYER_WHITE, difficulty=difficulty)
    def set_difficulty(self, difficulty: Difficulty) -> None:
        self.difficulty = difficulty
        if isinstance(self.ai, CheckersAI):
            self.ai.set_difficulty(difficulty)
    def initialize(self) -> None:
        if self.game_mode in (GAME_MODE_HUMAN_VS_AI, GAME_MODE_AI_VS_AI):
            self.ai.initialize()
        self.reset()
    def reset(self) -> None:
        self.board.reset()
        self.current_player = self.choose_starting_player()
        self.result.reset()
        self.game_state = GAME_RUNNING
        self.move_count = 0
        self.half_move_clock = 0
        self.in_multi_capture = False
        self.active_capture_piece = None
        self.state_manager.clear()
        self.human_player.reset()
        if self.game_mode == GAME_MODE_HUMAN_VS_AI:
            self.ai.set_player(PLAYER_WHITE)
        else:
            self.ai.set_player(self.current_player)
        self.ai.reset()
        if self.game_mode in (GAME_MODE_HUMAN_VS_AI, GAME_MODE_AI_VS_AI):
            self.ai.initialize()
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
        self.board_renderer.render(self.board,self.get_legal_moves(),self.human_player.get_selected_position(),self.active_capture_piece,)
        self.overlay_renderer.render(self)
    def make_move(self, *args: Any, **kwargs: Any) -> bool:
        if self.is_frozen():
            return False
        if not args:
            return False
        move = args[0] if len(args) == 1 else args
        if not isinstance(move, (tuple, list)) or len(move) != 4:
            return False
        move = tuple(move)
        if self.in_multi_capture:
            if not self._is_valid_multi_capture_move(move):
                return False
        else:
            if not CheckersRules.is_valid_move(self.board, move, self.current_player):
                return False
        from_row, from_column, to_row, to_column = move
        piece_before_move = self.board.get_cell(from_row, from_column)
        was_capture = CheckersRules.is_capture_move(move)
        captured_pieces = []
        if was_capture:
            mid_row = (from_row + to_row) // 2
            mid_col = (from_column + to_column) // 2
            captured_piece = self.board.get_cell(mid_row, mid_col)
            captured_pieces.append((mid_row, mid_col, captured_piece))
        if not CheckersRules.apply_move(self.board, move, self.current_player):
            return False
        piece_after_move = self.board.get_cell(to_row, to_column)
        was_promoted = CheckersRules.is_man(piece_before_move) and CheckersRules.is_king(piece_after_move)
        prev_half_move_clock = self.half_move_clock
        if was_capture:
            self.half_move_clock = 0
        else:
            self.half_move_clock += 1
        is_multi_turn = False
        if was_capture and not was_promoted:
            additional_captures = CheckersRules.get_capture_moves(self.board, to_row, to_column)
            if additional_captures:
                is_multi_turn = True
        record = MoveRecord(move=move,player=self.current_player,captured_pieces=captured_pieces,promoted_from=piece_before_move if was_promoted else None,promoted_to=piece_after_move if was_promoted else None,extra={"prev_in_multi_capture": self.in_multi_capture,"prev_active_piece": self.active_capture_piece,"prev_half_move_clock": prev_half_move_clock,"post_in_multi_capture": is_multi_turn,"post_active_piece": (to_row, to_column) if is_multi_turn else None,},)
        self.state_manager.push(record)
        self.move_count += 1
        self.event_manager.emit(EventType.ON_MOVE_MADE,move=move,player=self.current_player,was_capture=was_capture,move_count=self.move_count,)
        if was_capture:
            self.event_manager.emit(EventType.ON_PIECE_CAPTURED,captured_positions=[(cp[0], cp[1]) for cp in captured_pieces],player=self.current_player,)
            self.active_capture_piece = (to_row, to_column)
            if is_multi_turn:
                self.in_multi_capture = True
                return True
        self.in_multi_capture = False
        self.active_capture_piece = None
        self._finish_turn()
        return True
    def _is_valid_multi_capture_move(self, move: tuple[int, int, int, int]) -> bool:
        if self.active_capture_piece is None:
            return False
        from_row, from_column, _, _ = move
        active_row, active_column = self.active_capture_piece
        if from_row != active_row or from_column != active_column:
            return False
        capture_moves = CheckersRules.get_capture_moves(self.board, active_row, active_column)
        return move in capture_moves
    def _finish_turn(self) -> None:
        self.in_multi_capture = False
        self.active_capture_piece = None
        self.switch_player()
        if self.game_mode == GAME_MODE_AI_VS_AI:
            self.ai.set_player(self.current_player)
        self.event_manager.emit(EventType.ON_TURN_CHANGED, player=self.current_player)
        self.result = CheckersRules.evaluate_game(self.board, self.half_move_clock)
        if self.result.game_over:
            self.game_state = GAME_DRAW if self.result.draw else GAME_OVER
            self.event_manager.emit(EventType.ON_GAME_OVER,winner=self.result.winner,draw=self.result.draw,)
            return
        if not self.get_legal_moves():
            self.result.reset()
            self.result.game_over = True
            self.result.winner = (PLAYER_WHITE if self.current_player == PLAYER_BLACK else PLAYER_BLACK)
            self.game_state = GAME_OVER
            self.event_manager.emit(EventType.ON_GAME_OVER,winner=self.result.winner,draw=False,)
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
            from_r, from_c, to_r, to_c = record.move
            orig_piece = (record.promoted_from if record.promoted_from is not None else self.board.get_cell(to_r, to_c))
            self.board.set_cell(from_r, from_c, orig_piece)
            self.board.set_cell(to_r, to_c, EMPTY)
            for mr, mc, val in record.captured_pieces:
                self.board.set_cell(mr, mc, val)
            self.in_multi_capture = record.extra.get("prev_in_multi_capture", False)
            self.active_capture_piece = record.extra.get("prev_active_piece", None)
            self.half_move_clock = record.extra.get("prev_half_move_clock", 0)
            self.current_player = record.player
            self.move_count = max(0, self.move_count - 1)
        self.result = CheckersRules.evaluate_game(self.board, self.half_move_clock)
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
            from_r, from_c, to_r, to_c = move
            piece = (record.promoted_to if record.promoted_to is not None else self.board.get_cell(from_r, from_c))
            self.board.set_cell(to_r, to_c, piece)
            self.board.set_cell(from_r, from_c, EMPTY)
            for mr, mc, _ in record.captured_pieces:
                self.board.set_cell(mr, mc, EMPTY)
            if record.captured_pieces:
                self.half_move_clock = 0
            else:
                self.half_move_clock += 1
            self.move_count += 1
            if record.extra.get("post_in_multi_capture", False):
                self.in_multi_capture = True
                self.active_capture_piece = record.extra.get("post_active_piece", None)
            else:
                self.in_multi_capture = False
                self.active_capture_piece = None
                self._finish_turn()
            self.event_manager.emit(EventType.ON_MOVE_REDONE, move=move, player=record.player)
        return True
    def get_hint(self) -> tuple[int, int, int, int] | None:
        solver = CheckersAI(player=self.current_player, difficulty=Difficulty.IMPOSSIBLE)
        return solver.select_action(self.get_state())
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
        return None
    def update_current_player(self) -> None:
        controller = self.get_current_controller()
        if controller is None:
            return
        action = controller.get_action(self)
        if action is None:
            return
        if not isinstance(action, (tuple, list)) or len(action) != 4:
            return
        self.make_move(tuple(action))
    def get_legal_moves(self) -> list[tuple[int, int, int, int]]:
        if self.in_multi_capture:
            if self.active_capture_piece is None:
                return []
            row, column = self.active_capture_piece
            return CheckersRules.get_capture_moves(self.board, row, column)
        return CheckersRules.get_legal_moves(self.board, self.current_player)
    def get_valid_moves_for_cell(self, *position: int) -> list[tuple[int, int, int, int]]:
        if not position or len(position) < 2:
            return self.get_legal_moves()
        r, c = position[0], position[1]
        all_moves = self.get_legal_moves()
        return [m for m in all_moves if m[0] == r and m[1] == c]
    def get_state(self) -> dict[str, Any]:
        return {"board": self.board.get_board_state(),"current_player": self.current_player,"winner": self.result.winner,"game_state": self.game_state,"game_over": self.result.game_over,"draw": self.result.draw,"move_count": self.move_count,"in_multi_capture": self.in_multi_capture,"active_capture_piece": self.active_capture_piece,"legal_moves": self.get_legal_moves(),"black_count": self.board.count_pieces(PLAYER_BLACK),"white_count": self.board.count_pieces(PLAYER_WHITE),}
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
    def get_black_count(self) -> int:
        return self.board.count_pieces(PLAYER_BLACK)
    def get_white_count(self) -> int:
        return self.board.count_pieces(PLAYER_WHITE)
    def is_game_over(self) -> bool:
        return self.result.game_over
    def is_in_multi_capture(self) -> bool:
        return self.in_multi_capture
    def get_active_capture_piece(self) -> tuple[int, int] | None:
        return self.active_capture_piece
    def is_frozen(self) -> bool:
        return self.result.game_over