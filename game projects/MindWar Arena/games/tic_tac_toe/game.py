"""
MindWar Arena
Phase 2 - Tic-Tac-Toe

game.py
"""
import pygame

from engine.core.input import Input

from engine.interfaces.game_interface import GameInterface
from games.tic_tac_toe.overlay_renderer import OverlayRenderer
from games.tic_tac_toe.board_renderer import BoardRenderer
from games.tic_tac_toe.board import TicTacToeBoard
from games.tic_tac_toe.rules import TicTacToeRules
from games.tic_tac_toe.human_player import HumanPlayer
from engine.interfaces.game_result import GameResult
from games.tic_tac_toe.constants import (
    PLAYER_X,
    PLAYER_O,
    FIRST_PLAYER,
    NO_WINNER,
    GAME_NOT_STARTED,
    GAME_RUNNING,
    GAME_DRAW,
    GAME_OVER,
)


class TicTacToeGame(GameInterface):

    def __init__(self, renderer):

        self.renderer = renderer

        self.board = None

        self.current_player = FIRST_PLAYER

        self.result = GameResult()

        self.game_state = GAME_NOT_STARTED

        self.move_count = 0

        self.board_renderer = BoardRenderer(renderer)
        self.overlay_renderer = OverlayRenderer(renderer)
        self.human_player = HumanPlayer(self.board_renderer)

    # ---------------------------------------------------------

    def initialize(self):

        self.board = TicTacToeBoard()

        self.reset()

    # ---------------------------------------------------------

    def reset(self):

        if self.board is None:
            self.board = TicTacToeBoard()
        else:
            self.board.reset()
            
        self.current_player = FIRST_PLAYER
        self.result = GameResult()

        self.game_state = GAME_RUNNING
        self.move_count = 0

        self.board_renderer.reset()
        self.overlay_renderer.reset()

    # ---------------------------------------------------------

    def shutdown(self):
        pass

    # ---------------------------------------------------------

    def update(self):
        self.update_restart()
        if self.is_frozen():
            return

        self.update_players()

    # ---------------------------------------------------------

    def render(self):

        self.board_renderer.render(
            self.board,
            self.result,
        )
        self.overlay_renderer.render(
            self.result,
        )
    # ---------------------------------------------------------

    def make_move(self, row, column):

        if self.is_frozen():
            return False

        if not self.board.is_valid_position(row, column):
            return False

        if not self.board.is_cell_empty(row, column):
            return False

        self.board.set_cell(row, column, self.current_player)

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

    # ---------------------------------------------------------

    def switch_player(self):

        if self.current_player == PLAYER_X:
            self.current_player = PLAYER_O
        else:
            self.current_player = PLAYER_X

    # ---------------------------------------------------------

    def get_result(self):
        """
        Return the current game result.
        """

        return self.result
    
    def get_board(self):

        return self.board

    def get_current_player(self):

        return self.current_player

    def get_state(self):

        return {
            "board": self.board.get_board_state(),
            "current_player": self.current_player,
            "winner": self.result.winner,
            "game_state": self.game_state,
            "game_over": self.result.game_over,
            "draw": self.result.draw,
            "move_count": self.move_count,
        }

    def is_game_over(self):

        return self.is_frozen()

    def get_winner(self):

        return self.result.winner
    
    def is_frozen(self):

        """
        Returns True when the game state can no longer change.

        Once frozen:
        - No moves are accepted.
        - Current player never changes.
        - Winner never changes.
        - Board never changes.
        """

        return self.result.game_over
    
    # ---------------------------------------------------------

    def update_restart(self):
        """
        Restart the game after it has ended.

        Press R to begin a new match.
        """

        if not self.is_frozen():
            return

        if Input.is_key_clicked(pygame.K_r):
            self.reset()
            return
    
    def update_players(self):

        move = self.human_player.get_move(
            game_over=self.is_frozen(),
        )

        if move is None:
            return

        row, column = move

        self.make_move(
            row,
            column,
        )