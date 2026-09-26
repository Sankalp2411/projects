# games/othello/game.py
from engine.interfaces.game_interface import GameInterface
from engine.interfaces.game_result import GameResult
from games.othello.ai import OthelloAI
from games.othello.board import OthelloBoard
from games.othello.board_renderer import OthelloBoardRenderer
from games.othello.constants import (FIRST_PLAYER,GAME_DRAW,GAME_MODE_HUMAN_VS_AI,GAME_MODE_HUMAN_VS_HUMAN,GAME_MODE_AI_VS_AI,GAME_NOT_STARTED,GAME_OVER,GAME_RUNNING,PLAYER_BLACK,PLAYER_WHITE,)
from games.othello.human_player import HumanPlayer
from games.othello.overlay_renderer import OthelloOverlayRenderer
from games.othello.rules import OthelloRules
class OthelloGame(GameInterface):
    def __init__(self, renderer, game_mode=GAME_MODE_HUMAN_VS_HUMAN):
        self.renderer = renderer
        self.game_mode = game_mode
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
        self.ai = OthelloAI()
    def initialize(self):
        if self.game_mode in (GAME_MODE_HUMAN_VS_AI,GAME_MODE_AI_VS_AI,):
            self.ai.initialize()
        self.reset()
    def reset(self):
        self.board.reset()
        self.current_player = self.choose_starting_player()
        self.next_starting_player = (PLAYER_WHITE if self.current_player == PLAYER_BLACK else PLAYER_BLACK)
        self.result.reset()
        self.game_state = GAME_RUNNING
        self.move_count = 0
        self.consecutive_passes = 0
        self.board_renderer.reset()
        self.overlay_renderer.reset()
        if self.game_mode in (GAME_MODE_HUMAN_VS_AI,GAME_MODE_AI_VS_AI,):
            self.ai.reset()
            self.ai.initialize()
    def shutdown(self):
        pass
    def update(self):
        if self.is_frozen():
            return
        self.update_current_player()
    def render(self):
        self.board_renderer.render(self.renderer,self.board,self.result,)
        self.overlay_renderer.render(self.renderer,self.result,self.board,)
    def make_move(self, row, column):
        if self.is_frozen():
            return False
        if not self.board.is_valid_position(row, column):
            return False
        if not OthelloRules.is_valid_move(self.board,row,column,self.current_player,):
            return False
        if not OthelloRules.apply_move(self.board,row,column,self.current_player,):
            return False
        self.move_count += 1
        self.consecutive_passes = 0
        self.result = OthelloRules.evaluate_game(self.board)
        if self.result.game_over:
            self.game_state = GAME_DRAW if self.result.draw else GAME_OVER
            return True
        self.switch_player()
        if not self.get_legal_moves():
            self.pass_turn()
        return True
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
    def pass_turn(self):
        if self.is_frozen():
            return False
        if self.get_legal_moves():
            return False
        self.consecutive_passes += 1
        if self.consecutive_passes >= 2:
            self.result = OthelloRules.evaluate_game(self.board)
            self.game_state = (GAME_DRAW if self.result.draw else GAME_OVER)
            return True
        self.switch_player()
        return True
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
        if len(action) != 2:
            return
        row, column = action
        self.make_move(row, column)
    def get_state(self):
        return {"board": self.board.get_board_state(),"current_player": self.current_player,"winner": self.result.winner,"game_state": self.game_state,"game_over": self.result.game_over,"draw": self.result.draw,"move_count": self.move_count,"consecutive_passes": self.consecutive_passes,"black_count": self.board.count_stones(PLAYER_BLACK),"white_count": self.board.count_stones(PLAYER_WHITE),"legal_moves": self.get_legal_moves(),}
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
    def get_legal_moves(self):
        return OthelloRules.get_legal_moves(self.board,self.current_player,)
    def get_black_count(self):
        return self.board.count_stones(PLAYER_BLACK)
    def get_white_count(self):
        return self.board.count_stones(PLAYER_WHITE)
    def is_game_over(self):
        return self.result.game_over
    def is_frozen(self):
        return self.result.game_over