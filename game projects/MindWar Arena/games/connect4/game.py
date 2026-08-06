import pygame

from engine.core.input import Input
from engine.interfaces.game_interface import GameInterface
from engine.interfaces.game_result import GameResult

from games.connect4.ai import Connect4AI
from games.connect4.board import Connect4Board
from games.connect4.board_renderer import BoardRenderer
from games.connect4.human_player import HumanPlayer
from games.connect4.overlay_renderer import OverlayRenderer
from games.connect4.rules import Connect4Rules

from games.connect4.constants import (
    PLAYER_RED,
    PLAYER_YELLOW,
    FIRST_PLAYER,
    GAME_NOT_STARTED,
    GAME_RUNNING,
    GAME_DRAW,
    GAME_OVER,
    GAME_MODE_HUMAN_VS_HUMAN,
    GAME_MODE_HUMAN_VS_AI,
)


class Connect4Game(GameInterface):
    def __init__(self, renderer,game_mode=GAME_MODE_HUMAN_VS_HUMAN,):
        self.renderer = renderer
        self.game_mode = game_mode
        self.board = Connect4Board()

        self.current_player = FIRST_PLAYER
        self.next_starting_player = FIRST_PLAYER

        self.result = GameResult()

        self.game_state = GAME_NOT_STARTED
        self.move_count = 0

        self.board_renderer = BoardRenderer(renderer)
        self.overlay_renderer = OverlayRenderer(renderer)

        self.human_player = HumanPlayer(self.board_renderer)
        self.ai_player = Connect4AI()

        self.player_red = self.human_player
        if self.game_mode == GAME_MODE_HUMAN_VS_AI:
            self.player_yellow = self.ai_player
        else:
            self.player_yellow = self.human_player

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
        self.update_restart()

        if self.is_frozen():
            return

        self.update_current_player()

    def render(self):
        self.board_renderer.render(
            self.board,
            self.result,
        )

        self.overlay_renderer.render(self.result)

    def make_move(self, column):
        if self.is_frozen():
            return False

        if column is None:
            return False

        row = self.board.drop_piece(
            column,
            self.current_player,
        )

        if row is None:
            return False

        self.move_count += 1

        self.result = Connect4Rules.evaluate_game(
            self.board
        )

        if self.result.game_over:

            if self.result.draw:
                self.game_state = GAME_DRAW

            else:
                self.game_state = GAME_OVER

            return True

        self.switch_player()

        return True

    def switch_player(self):
        if self.current_player == PLAYER_RED:
            self.current_player = PLAYER_YELLOW
        else:
            self.current_player = PLAYER_RED

    def choose_starting_player(self):
        self.current_player = self.next_starting_player

        if self.next_starting_player == PLAYER_RED:
            self.next_starting_player = PLAYER_YELLOW
        else:
            self.next_starting_player = PLAYER_RED

    def get_current_controller(self):
        if self.current_player == PLAYER_RED:
            return self.player_red

        return self.player_yellow

    def update_current_player(self):
        controller = self.get_current_controller()

        move = controller.get_action(self)

        if move is None:
            return

        self.make_move(move)

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
        return self.result.game_over