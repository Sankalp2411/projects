"""
MindWar Arena
Phase 2 - Tic-Tac-Toe

game.py

Implements the Tic-Tac-Toe game controller.

Responsibilities:
- Manage the board.
- Manage player turns.
- Validate and apply moves.
- Detect wins and draws.
- Maintain game state.
- Expose state for AI and rendering.

This module does NOT:
- Render graphics.
- Handle mouse/keyboard input.
- Implement AI logic.
"""

from engine.interfaces.game_interface import GameInterface

from games.tic_tac_toe.board_renderer import BoardRenderer
from games.tic_tac_toe.board import TicTacToeBoard
from games.tic_tac_toe.rules import TicTacToeRules

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
    """
    Main controller for a Tic-Tac-Toe match.
    """

    def __init__(self, renderer):
        """
        Create a new Tic-Tac-Toe game.
        """

        self.renderer = renderer

        self.board = None

        self.current_player = FIRST_PLAYER

        self.winner = NO_WINNER

        self.game_state = GAME_NOT_STARTED

        self.game_over = False

        self.move_count = 0

        self.board_renderer = BoardRenderer(renderer)

    # ---------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------

    def initialize(self):
        """
        Initialize a new game.
        """

        self.board = TicTacToeBoard()

        self.reset()

    def reset(self):
        """
        Reset the game to its initial state.
        """

        if self.board is None:
            self.board = TicTacToeBoard()
        else:
            self.board.reset()

        self.current_player = FIRST_PLAYER

        self.winner = NO_WINNER

        self.game_state = GAME_RUNNING

        self.game_over = False

        self.move_count = 0

    def shutdown(self):
        """
        Shutdown the game.

        Reserved for future cleanup.
        """

        pass

    # ---------------------------------------------------------
    # Game Loop
    # ---------------------------------------------------------

    def update(self):
        """
        Reserved for future gameplay updates.

        Human input, AI turns, animations,
        timers, etc. will be added later.
        """

        pass

    def render(self):
        """
        Render the current board.
        """

        self.board_renderer.render(self.board)

    # ---------------------------------------------------------
    # Gameplay
    # ---------------------------------------------------------

    def make_move(self, row, column):
        """
        Attempt to place the current player's mark.

        Returns
        -------
        bool
            True if successful.
            False otherwise.
        """

        if self.game_over:
            return False

        if not self.board.is_valid_position(row, column):
            return False

        if not self.board.is_cell_empty(row, column):
            return False

        self.board.set_cell(row, column, self.current_player)

        self.move_count += 1

        winner = TicTacToeRules.check_winner(self.board)

        if winner != NO_WINNER:

            self.winner = winner

            self.game_state = GAME_OVER

            self.game_over = True

            return True

        if TicTacToeRules.is_draw(self.board):

            self.winner = NO_WINNER

            self.game_state = GAME_DRAW

            self.game_over = True

            return True

        self.switch_player()

        return True

    def switch_player(self):
        """
        Switch the active player.
        """

        if self.current_player == PLAYER_X:
            self.current_player = PLAYER_O
        else:
            self.current_player = PLAYER_X

    # ---------------------------------------------------------
    # State Access
    # ---------------------------------------------------------

    def get_board(self):
        """
        Return the board.
        """

        return self.board

    def get_current_player(self):
        """
        Return the active player.
        """

        return self.current_player

    def get_state(self):
        """
        Return the current game state.
        """

        return {
            "board": self.board.get_board_state(),
            "current_player": self.current_player,
            "winner": self.winner,
            "game_state": self.game_state,
            "game_over": self.game_over,
            "move_count": self.move_count,
        }

    def is_game_over(self):
        """
        Return whether the game has finished.
        """

        return self.game_over

    def get_winner(self):
        """
        Return the winning player.
        """

        return self.winner