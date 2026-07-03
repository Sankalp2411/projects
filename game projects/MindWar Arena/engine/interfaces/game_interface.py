"""
MindWar Arena

game_interface.py

Defines the universal interface that every game inside
MindWar Arena must implement.

Examples
--------
- Tic-Tac-Toe
- Connect Four
- Gomoku
- Pente
- Othello
- Checkers
- Chess
- Nine Men's Morris
- Go

The engine communicates only through this interface.
"""

from abc import ABC
from abc import abstractmethod


class GameInterface(ABC):

    # ---------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------

    @abstractmethod
    def initialize(self):
        """
        Initialize the game.
        """
        pass

    @abstractmethod
    def reset(self):
        """
        Reset the game to its initial state.
        """
        pass

    @abstractmethod
    def shutdown(self):
        """
        Release resources before closing.
        """
        pass

    # ---------------------------------------------------------
    # Game Loop
    # ---------------------------------------------------------

    @abstractmethod
    def update(self):
        """
        Update one frame of gameplay.
        """
        pass

    @abstractmethod
    def render(self):
        """
        Render one frame.
        """
        pass

    # ---------------------------------------------------------
    # State
    # ---------------------------------------------------------

    @abstractmethod
    def get_state(self):
        """
        Return the current game state.
        """
        pass

    @abstractmethod
    def get_board(self):
        """
        Return the board object.
        """
        pass

    @abstractmethod
    def get_current_player(self):
        """
        Return the player whose turn it is.
        """
        pass

    @abstractmethod
    def get_winner(self):
        """
        Return the winner.
        """
        pass

    @abstractmethod
    def is_game_over(self):
        """
        Return True if the game has finished.
        """
        pass

    # ---------------------------------------------------------
    # Gameplay
    # ---------------------------------------------------------

    @abstractmethod
    def make_move(self, *args, **kwargs):
        """
        Execute one move.
        """
        pass