#games/tic_tac_toe/game.py
import pygame
from engine.core.input import Input
from games.tic_tac_toe.ai import TicTacToeAI
from engine.interfaces.game_interface import GameInterface
from games.tic_tac_toe.overlay_renderer import OverlayRenderer
from games.tic_tac_toe.board_renderer import BoardRenderer
from games.tic_tac_toe.board import TicTacToeBoard
from games.tic_tac_toe.rules import TicTacToeRules
from games.tic_tac_toe.human_player import HumanPlayer
from engine.interfaces.game_result import GameResult
from games.tic_tac_toe.constants import (PLAYER_X,PLAYER_O,FIRST_PLAYER,GAME_NOT_STARTED,GAME_RUNNING,GAME_DRAW,GAME_OVER,)
class TicTacToeGame(GameInterface):
    def __init__(self, renderer):
        self.renderer = renderer
        self.board = TicTacToeBoard()
        self.current_player = FIRST_PLAYER
        self.next_starting_player = FIRST_PLAYER
        self.result = GameResult()
        self.game_state = GAME_NOT_STARTED
        self.move_count = 0
        self.board_renderer = BoardRenderer(renderer)
        self.overlay_renderer = OverlayRenderer(renderer)
        self.human_player = HumanPlayer(self.board_renderer)
        self.ai_player = TicTacToeAI()
        self.player_x = self.human_player
        self.player_o = self.ai_player
    def initialize(self):
        self.ai_player.initialize()
        self.reset()
    def reset(self):
        self.board.reset()
        self.choose_starting_player()
        self.result = GameResult()
        self.ai_player.reset()
        self.ai_player.initialize()
        self.game_state = GAME_RUNNING
        self.move_count = 0
        self.board_renderer.reset()
        self.overlay_renderer.reset()
    def shutdown(self):
        pass
    def update(self):
        self.update_restart()
        if self.is_frozen():
            return
        self.update_current_player()
    def render(self):
        self.board_renderer.render(self.board,self.result,)
        self.overlay_renderer.render(self.result,)
    def make_move(self, row, column):
        if self.is_frozen():
            return False
        if not self.board.is_valid_position(row, column):
            return False
        if not self.board.is_cell_empty(row, column):
            return False
        self.board.set_cell(row,column,self.current_player,)
        self.move_count += 1
        self.result = TicTacToeRules.evaluate_game(self.board)
        if self.result.game_over:
            if self.result.draw:
                self.game_state = GAME_DRAW
            else:
                self.game_state = GAME_OVER
            return True
        self.switch_player()
        return True
    def switch_player(self):
        if self.current_player == PLAYER_X:
            self.current_player = PLAYER_O
        else:
            self.current_player = PLAYER_X
    def choose_starting_player(self):
        self.current_player = self.next_starting_player
        if self.next_starting_player == PLAYER_X:
            self.next_starting_player = PLAYER_O
        else:
            self.next_starting_player = PLAYER_X
    def get_current_controller(self):
        if self.current_player == PLAYER_X:
            return self.player_x
        return self.player_o
    def update_current_player(self):
        controller = self.get_current_controller()
        move = controller.get_action(self)
        if move is None:
            return
        self.make_move(*move)
    def update_restart(self):
        if not self.is_frozen():
            return
        if Input.is_key_clicked(pygame.K_r):
            self.reset()
    def get_result(self):
        return self.result
    def get_board(self):
        return self.board
    def get_current_player(self):
        return self.current_player
    def get_state(self):
        return {"board": self.board.get_board_state(),"current_player": self.current_player,"winner": self.result.winner,"game_state": self.game_state,"game_over": self.result.game_over,"draw": self.result.draw,"move_count": self.move_count,}
    def is_game_over(self):
        return self.is_frozen()
    def get_winner(self):
        return self.result.winner
    def is_frozen(self):
        return self.result.game_over