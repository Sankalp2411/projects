"""
MindWar Arena

game_result.py

Universal game result container.

Responsibilities
----------------
• Store the outcome of a finished or running game.
• Provide a consistent interface for every game.
• Remain independent of any specific game implementation.

Supported Games
---------------
- Tic-Tac-Toe
- Connect Four
- Gomoku
- Pente
- Othello
- Checkers
- Chess
- Go
- Future games

This class contains only game-result data.
It never performs game logic.
"""


class GameResult:
    """
    Universal container describing the current result of a game.
    """

    def __init__(self):
        """
        Create a default game result.
        """

        # Winner of the game.
        # None means no winner yet.
        self.winner = None

        # True once the match has ended.
        self.game_over = False

        # True only if the match ended in a draw.
        self.draw = False

        # Cells responsible for the victory.
        #
        # Example:
        # [(0,0), (0,1), (0,2)]
        #
        # Games that do not use board cells
        # may simply leave this empty.
        self.winning_cells = []

    # ---------------------------------------------------------
    # Utility
    # ---------------------------------------------------------

    def reset(self):
        """
        Restore the default running state.
        """

        self.winner = None
        self.game_over = False
        self.draw = False
        self.winning_cells.clear()

    def has_winner(self):
        """
        Return True if a winner exists.
        """

        return self.winner is not None

    def is_draw(self):
        """
        Return True if the match ended in a draw.
        """

        return self.draw

    def is_game_over(self):
        """
        Return True if the match has finished.
        """

        return self.game_over