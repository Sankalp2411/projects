# games/gomoku/game.py
from engine.interfaces.game_interface import GameInterface
from engine.interfaces.game_result import GameResult
from games.gomoku.ai import GomokuAI
from games.gomoku.board import GomokuBoard
from games.gomoku.board_renderer import BoardRenderer
from games.gomoku.human_player import HumanPlayer
from games.gomoku.overlay_renderer import OverlayRenderer
from games.gomoku.rules import GomokuRules
from games.gomoku.constants import (PLAYER_BLACK, PLAYER_WHITE, FIRST_PLAYER, GAME_NOT_STARTED, GAME_RUNNING, GAME_DRAW, GAME_OVER, GAME_MODE_HUMAN_VS_HUMAN, GAME_MODE_HUMAN_VS_AI,)
class GomokuGame(GameInterface):
    def __init__(self,renderer,game_mode=GAME_MODE_HUMAN_VS_HUMAN,):
        self.renderer = renderer
        self.game_mode = game_mode
        self.board = GomokuBoard()
        self.current_player = FIRST_PLAYER
        self.next_starting_player = FIRST_PLAYER
        self.result = GameResult()
        self.game_state = GAME_NOT_STARTED
        self.move_count = 0
        self.board_renderer = BoardRenderer(renderer)
        self.overlay_renderer = OverlayRenderer(renderer)
        self.human_player = HumanPlayer(self.board_renderer)
        self.ai_player = GomokuAI()
        self.player_black = self.human_player
        if self.game_mode == GAME_MODE_HUMAN_VS_AI:
            self.player_white = self.ai_player
        else:
            self.player_white = self.human_player
    def initialize(self):
        if self.game_mode == GAME_MODE_HUMAN_VS_AI:
            self.ai_player.initialize()
        self.reset()
    def reset(self):
        self.board.reset()
        self.choose_starting_player()
        self.result = GameResult()
        if self.game_mode == GAME_MODE_HUMAN_VS_AI:
            self.ai_player.reset()
            self.ai_player.initialize()
        self.game_state = GAME_RUNNING
        self.move_count = 0
        self.board_renderer.reset()
        self.overlay_renderer.reset()
    def shutdown(self):
        pass
    def update(self):
        if self.is_frozen():
            return
        self.update_current_player()
    def render(self):
        self.board_renderer.render(self.board,self.result,)
        self.overlay_renderer.render(self.result)
    def make_move(self, row, column):
        if self.is_frozen():
            return False
        if not self.board.is_valid_position(row,column,):
            return False
        if not self.board.is_cell_empty(row,column,):
            return False
        self.board.set_cell(row,column,self.current_player,)
        self.move_count += 1
        self.result = GomokuRules.evaluate_game(self.board)
        if self.result.game_over:
            if self.result.draw:
                self.game_state = GAME_DRAW
            else:
                self.game_state = GAME_OVER
            return True
        self.switch_player()
        return True
    def switch_player(self):
        if self.current_player == PLAYER_BLACK:
            self.current_player = PLAYER_WHITE
        else:
            self.current_player = PLAYER_BLACK
    def choose_starting_player(self):
        self.current_player = (self.next_starting_player)
        if self.next_starting_player == PLAYER_BLACK:
            self.next_starting_player = PLAYER_WHITE
        else:
            self.next_starting_player = PLAYER_BLACK
    def get_current_controller(self):
        if self.current_player == PLAYER_BLACK:
            return self.player_black
        return self.player_white
    def update_current_player(self):
        controller = self.get_current_controller()
        move = controller.get_action(self)
        if move is None:
            return
        self.make_move(*move)
    def get_result(self):
        return self.result
    def get_board(self):
        return self.board
    def get_current_player(self):
        return self.current_player
    def get_state(self):
        return {"board": self.board.get_board_state(), "current_player": self.current_player, "winner": self.result.winner, "game_state": self.game_state, "game_over": self.result.game_over, "draw": self.result.draw, "move_count": self.move_count,}
    def is_game_over(self):
        return self.is_frozen()
    def get_winner(self):
        return self.result.winner
    def is_frozen(self):
        return self.result.game_over