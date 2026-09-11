# games/checkers/game.py
from engine.interfaces.game_interface import GameInterface
from engine.interfaces.game_result import GameResult
from games.checkers.ai import CheckersAI
from games.checkers.board import CheckersBoard
from games.checkers.board_renderer import CheckersBoardRenderer
from games.checkers.constants import (FIRST_PLAYER,GAME_DRAW,GAME_MODE_AI_VS_AI,GAME_MODE_HUMAN_VS_AI,GAME_MODE_HUMAN_VS_HUMAN,GAME_NOT_STARTED,GAME_OVER,GAME_RUNNING,PLAYER_BLACK,PLAYER_WHITE,)
from games.checkers.human_player import HumanPlayer
from games.checkers.overlay_renderer import CheckersOverlayRenderer
from games.checkers.rules import CheckersRules
class CheckersGame(GameInterface):
    def __init__(self,renderer,game_mode=GAME_MODE_HUMAN_VS_HUMAN,):
        self.renderer = renderer
        self.game_mode = game_mode
        self.board = CheckersBoard()
        self.current_player = FIRST_PLAYER
        self.next_starting_player = FIRST_PLAYER
        self.result = GameResult()
        self.game_state = GAME_NOT_STARTED
        self.move_count = 0
        self.in_multi_capture = False
        self.active_capture_piece = None
        self.board_renderer = CheckersBoardRenderer(renderer)
        self.overlay_renderer = CheckersOverlayRenderer(renderer)
        self.human_player = HumanPlayer(self.board_renderer)
        self.ai = CheckersAI(FIRST_PLAYER)
    def initialize(self):
        if self.game_mode in (GAME_MODE_HUMAN_VS_AI,GAME_MODE_AI_VS_AI,):
            self.ai.initialize()
        self.reset()
    def reset(self):
        self.board.reset()
        self.current_player = (self.choose_starting_player())
        self.result.reset()
        self.game_state = GAME_RUNNING
        self.move_count = 0
        self.in_multi_capture = False
        self.active_capture_piece = None
        self.human_player.reset()
        self.ai.set_player(self.current_player)
        self.ai.reset()
        if self.game_mode in (GAME_MODE_HUMAN_VS_AI,GAME_MODE_AI_VS_AI,):
            self.ai.initialize()
        self.board_renderer.reset()
        self.overlay_renderer.reset()
    def shutdown(self):
        pass
    def update(self):
        if self.is_frozen():
            return
        self.update_current_player()
    def render(self):
        self.board_renderer.render(self.board,self.get_legal_moves(),self.human_player.get_selected_position(),self.active_capture_piece,)
        self.overlay_renderer.render(self)
    def make_move(self, move):
        if self.is_frozen():
            return False
        if not isinstance(move, tuple):
            return False
        if len(move) != 4:
            return False
        if self.in_multi_capture:
            if not self._is_valid_multi_capture_move(move):
                return False
        else:
            if not CheckersRules.is_valid_move(self.board,move,self.current_player,):
                return False
        from_row, from_column, to_row, to_column = move
        piece_before_move = self.board.get_cell(from_row,from_column,)
        if not CheckersRules.apply_move(self.board,move,self.current_player,):
            return False
        piece_after_move = self.board.get_cell(to_row,to_column,)
        self.move_count += 1
        was_capture = CheckersRules.is_capture_move(move)
        if was_capture:
            self.active_capture_piece = (to_row,to_column,)
            if (CheckersRules.is_man(piece_before_move) and CheckersRules.is_king(piece_after_move)):
                self.in_multi_capture = False
                self.active_capture_piece = None
                self._finish_turn()
                return True
            additional_captures = (CheckersRules.get_capture_moves(self.board,to_row,to_column,))
            if additional_captures:
                self.in_multi_capture = True
                return True
        self.in_multi_capture = False
        self.active_capture_piece = None
        self._finish_turn()
        return True
    def _is_valid_multi_capture_move(self, move):
        if self.active_capture_piece is None:
            return False
        from_row, from_column, _, _ = move
        active_row, active_column = (self.active_capture_piece)
        if (from_row != active_row or from_column != active_column):
            return False
        capture_moves = (CheckersRules.get_capture_moves(self.board,active_row,active_column,))
        return move in capture_moves
    def _finish_turn(self):
        self.in_multi_capture = False
        self.active_capture_piece = None
        self.switch_player()
        self.ai.set_player(self.current_player)
        self.result = CheckersRules.evaluate_game(self.board)
        if self.result.game_over:
            if self.result.draw:
                self.game_state = GAME_DRAW
            else:
                self.game_state = GAME_OVER
            return
        if not self.get_legal_moves():
            self.result.reset()
            self.result.game_over = True
            self.result.winner = (PLAYER_WHITE if self.current_player == PLAYER_BLACK else PLAYER_BLACK)
            self.game_state = GAME_OVER
    def switch_player(self):
        if self.current_player == PLAYER_BLACK:
            self.current_player = PLAYER_WHITE
        else:
            self.current_player = PLAYER_BLACK
    def choose_starting_player(self):
        player = self.next_starting_player
        if player == PLAYER_BLACK:
            self.next_starting_player = PLAYER_WHITE
        else:
            self.next_starting_player = PLAYER_BLACK
        return player
    def get_current_controller(self):
        if self.game_mode == GAME_MODE_HUMAN_VS_HUMAN:
            return self.human_player
        if self.game_mode == GAME_MODE_HUMAN_VS_AI:
            if self.current_player == PLAYER_BLACK:
                return self.human_player
            return self.ai
        if self.game_mode == GAME_MODE_AI_VS_AI:
            return self.ai
        return None
    def update_current_player(self):
        controller = self.get_current_controller()
        if controller is None:
            return
        action = controller.get_action(self)
        if action is None:
            return
        if not isinstance(action, tuple):
            return
        if len(action) != 4:
            return
        self.make_move(action)
    def get_legal_moves(self):
        if self.in_multi_capture:
            if self.active_capture_piece is None:
                return []
            row, column = self.active_capture_piece
            return CheckersRules.get_capture_moves(self.board,row,column,)
        return CheckersRules.get_legal_moves(self.board,self.current_player,)
    def get_state(self):
        return {"board": self.board.get_board_state(),"current_player": self.current_player,"winner": self.result.winner,"game_state": self.game_state,"game_over": self.result.game_over,"draw": self.result.draw,"move_count": self.move_count,"in_multi_capture": self.in_multi_capture,"active_capture_piece": (self.active_capture_piece),"legal_moves": self.get_legal_moves(),"black_count": self.board.count_pieces(PLAYER_BLACK),"white_count": self.board.count_pieces(PLAYER_WHITE),}
    def get_board(self):
        return self.board
    def get_current_player(self):
        return self.current_player
    def get_winner(self):
        return self.result.winner
    def get_result(self):
        return self.result
    def get_game_state(self):
        return self.game_state
    def get_black_count(self):
        return self.board.count_pieces(PLAYER_BLACK)
    def get_white_count(self):
        return self.board.count_pieces(PLAYER_WHITE)
    def is_game_over(self):
        return self.result.game_over
    def is_in_multi_capture(self):
        return self.in_multi_capture
    def get_active_capture_piece(self):
        return self.active_capture_piece
    def is_frozen(self):
        return self.result.game_over