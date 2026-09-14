# games/chess/game.py
from engine.interfaces.game_interface import GameInterface
from engine.interfaces.game_result import GameResult
from games.chess.ai import ChessAI
from games.chess.board import ChessBoard
from games.chess.board_renderer import ChessBoardRenderer
from games.chess.constants import (BLACK_KING,BLACK_ROOK,FIRST_PLAYER,GAME_DRAW,GAME_MODE_AI_VS_AI,GAME_MODE_HUMAN_VS_AI,GAME_MODE_HUMAN_VS_HUMAN,GAME_NOT_STARTED,GAME_OVER,GAME_RUNNING,PLAYER_BLACK,PLAYER_WHITE,WHITE_KING,WHITE_ROOK,)
from games.chess.human_player import HumanPlayer
from games.chess.overlay_renderer import ChessOverlayRenderer
from games.chess.rules import ChessRules
class ChessGame(GameInterface):
    def __init__(self,renderer,game_mode=GAME_MODE_HUMAN_VS_HUMAN,):
        self.renderer = renderer
        self.game_mode = game_mode
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
        self.en_passant_target = None
        self.white_controller = None
        self.black_controller = None
        self._create_controllers()
    def initialize(self):
        self.reset()
    def reset(self):
        self.board.reset()
        self.current_player = (self.choose_starting_player())
        self.result.reset()
        self.game_state = GAME_RUNNING
        self.position_state = "NORMAL"
        self.move_count = 0
        self.half_move_clock = 0
        self.last_move = None
        self.castling_rights = {"white_kingside": True,"white_queenside": True,"black_kingside": True,"black_queenside": True,}
        self.en_passant_target = None
        self.board_renderer.reset()
        self.overlay_renderer.reset()
        self._reset_controllers()
    def shutdown(self):
        pass
    def _create_controllers(self):
        if self.game_mode == GAME_MODE_HUMAN_VS_HUMAN:
            self.white_controller = HumanPlayer(self.board_renderer)
            self.black_controller = HumanPlayer(self.board_renderer)
        elif self.game_mode == GAME_MODE_HUMAN_VS_AI:
            self.white_controller = HumanPlayer(self.board_renderer)
            self.black_controller = ChessAI(PLAYER_BLACK)
        elif self.game_mode == GAME_MODE_AI_VS_AI:
            self.white_controller = ChessAI(PLAYER_WHITE)
            self.black_controller = ChessAI(PLAYER_BLACK)
        else:
            raise ValueError(f"Invalid Chess game mode: "f"{self.game_mode}")
    def _reset_controllers(self):
        if self.white_controller is not None:
            if hasattr(self.white_controller,"reset",):
                self.white_controller.reset()
        if self.black_controller is not None:
            if hasattr(self.black_controller,"reset",):
                self.black_controller.reset()
    def update(self):
        if self.is_frozen():
            return
        self.update_current_player()
    def render(self):
        if self.board_renderer is None:
            return
        check_position = (self._get_check_position())
        selected_position = (self._get_selected_position())
        self.board_renderer.render(board=self.board,legal_moves=self.get_legal_moves(),selected_position=selected_position,last_move=self.last_move,check_position=check_position,en_passant_target=self.en_passant_target,)
        self._render_overlay()
    def _render_overlay(self):
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
            self.overlay_renderer.draw_game_over(winner=self.result.winner,draw=self.result.draw,)
            return
        if self.position_state == "CHECK":
            self.overlay_renderer.draw_check()
    def make_move(self, move):
        if self.is_frozen():
            return False
        if not isinstance(move, tuple):
            return False
        if len(move) not in (4, 5):
            return False
        if not ChessRules.is_valid_move(self.board,move,self.current_player,self.en_passant_target,self.castling_rights,):
            return False
        (from_row,from_column,to_row,to_column,) = move[:4]
        piece = self.board.get_cell(from_row,from_column,)
        is_capture = ChessRules.is_capture_move(self.board,move,self.current_player,self.en_passant_target,self.castling_rights,)
        if is_capture or ChessRules.is_pawn(piece):
            self.half_move_clock = 0
        else:
            self.half_move_clock += 1
        if not ChessRules.apply_move(self.board,move,self.current_player,self.en_passant_target,self.castling_rights,):
            return False
        self.move_count += 1
        self.last_move = move
        self._update_castling_rights(piece,move,)
        self._update_en_passant(piece,move,)
        self.switch_player()
        self._evaluate_position()
        return True
    def switch_player(self):
        if self.current_player == PLAYER_WHITE:
            self.current_player = PLAYER_BLACK
        else:
            self.current_player = PLAYER_WHITE
    def choose_starting_player(self):
        player = self.next_starting_player
        if player == PLAYER_WHITE:
            self.next_starting_player = PLAYER_BLACK
        else:
            self.next_starting_player = PLAYER_WHITE
        return player
    def get_current_controller(self):
        if self.current_player == PLAYER_WHITE:
            return self.white_controller
        if self.current_player == PLAYER_BLACK:
            return self.black_controller
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
        if len(action) not in (4, 5):
            return
        self.make_move(action)
    def get_legal_moves(self):
        return ChessRules.get_legal_moves(self.board,self.current_player,self.en_passant_target,self.castling_rights,)
    def _get_selected_position(self):
        controller = (self.get_current_controller())
        if controller is None:
            return None
        if hasattr(controller,"get_selected_position",):
            return controller.get_selected_position()
        return None
    def _get_check_position(self):
        if self.result.game_over:
            return None
        if not ChessRules.is_in_check(self.board,self.current_player,):
            return None
        return self.board.find_king(self.current_player)
    def get_board_renderer(self):
        return self.board_renderer
    def get_overlay_renderer(self):
        return self.overlay_renderer
    def _update_castling_rights(self,piece,move,):
        (from_row,from_column,to_row,to_column,) = move[:4]
        if piece == WHITE_KING:
            self.castling_rights["white_kingside"] = False
            self.castling_rights["white_queenside"] = False
        elif piece == BLACK_KING:
            self.castling_rights["black_kingside"] = False
            self.castling_rights["black_queenside"] = False
        elif piece == WHITE_ROOK:
            if (from_row == 7 and from_column == 0):
                self.castling_rights["white_queenside"] = False
            elif (from_row == 7 and from_column == 7):
                self.castling_rights["white_kingside"] = False
        elif piece == BLACK_ROOK:
            if (from_row == 0 and from_column == 0):
                self.castling_rights["black_queenside"] = False
            elif (from_row == 0 and from_column == 7):
                self.castling_rights["black_kingside"] = False
        if (to_row == 7 and to_column == 0):
            self.castling_rights["white_queenside"] = False
        elif (to_row == 7 and to_column == 7):
            self.castling_rights["white_kingside"] = False
        elif (to_row == 0 and to_column == 0):
            self.castling_rights["black_queenside"] = False
        elif (to_row == 0 and to_column == 7):
            self.castling_rights["black_kingside"] = False
    def _update_en_passant(self,piece,move,):
        self.en_passant_target = None
        if not ChessRules.is_pawn(piece):
            return
        (from_row,from_column,to_row,to_column,) = move[:4]
        if abs(to_row - from_row) == 2:
            self.en_passant_target = ((from_row + to_row) // 2,from_column,)
    def _evaluate_position(self):
        self.result.reset()
        self.position_state = "NORMAL"
        white_king = self.board.find_king(PLAYER_WHITE)
        black_king = self.board.find_king(PLAYER_BLACK)
        if white_king is None:
            self.result.game_over = True
            self.result.draw = False
            self.result.winner = PLAYER_BLACK
            self.game_state = GAME_OVER
            self.position_state = "CHECKMATE"
            return
        if black_king is None:
            self.result.game_over = True
            self.result.draw = False
            self.result.winner = PLAYER_WHITE
            self.game_state = GAME_OVER
            self.position_state = "CHECKMATE"
            return
        legal_moves = ChessRules.get_legal_moves(self.board,self.current_player,self.en_passant_target,self.castling_rights,)
        current_player_in_check = (ChessRules.is_in_check(self.board,self.current_player,))
        if not legal_moves:
            if current_player_in_check:
                if self.current_player == PLAYER_WHITE:
                    self.result.winner = PLAYER_BLACK
                else:
                    self.result.winner = PLAYER_WHITE
                self.result.game_over = True
                self.result.draw = False
                self.game_state = GAME_OVER
                self.position_state = "CHECKMATE"
            else:
                self.result.winner = None
                self.result.game_over = True
                self.result.draw = True
                self.game_state = GAME_DRAW
                self.position_state = "STALEMATE"
            return
        self.result.game_over = False
        self.result.draw = False
        self.result.winner = None
        self.game_state = GAME_RUNNING
        if current_player_in_check:
            self.position_state = "CHECK"
        else:
            self.position_state = "NORMAL"
    def get_state(self):
        return {"board": self.board.get_board_state(),"current_player": self.current_player,"winner": self.result.winner,"game_state": self.game_state,"position_state": self.position_state,"game_over": self.result.game_over,"draw": self.result.draw,"move_count": self.move_count,"half_move_clock": self.half_move_clock,"last_move": self.last_move,"castling_rights": dict(self.castling_rights),"en_passant_target": (self.en_passant_target),"legal_moves": self.get_legal_moves(),}
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
    def get_position_state(self):
        return self.position_state
    def get_move_count(self):
        return self.move_count
    def get_half_move_clock(self):
        return self.half_move_clock
    def get_last_move(self):
        return self.last_move
    def get_castling_rights(self):
        return dict(self.castling_rights)
    def get_en_passant_target(self):
        return self.en_passant_target
    def is_game_over(self):
        return self.result.game_over
    def is_frozen(self):
        return self.result.game_over
    def is_draw(self):
        return self.result.draw
    def set_draw(self):
        self.result.reset()
        self.result.game_over = True
        self.result.draw = True
        self.result.winner = None
        self.game_state = GAME_DRAW
        self.position_state = "NORMAL"