"""
MindWar Arena
Phase 2 - Tic-Tac-Toe

rules.py

This module implements the complete rule engine for Tic-Tac-Toe.

Responsibilities:
- Detect winning conditions.
- Detect draw conditions.
- Detect game-over conditions.

This module does NOT:
- Modify the board.
- Handle player turns.
- Render graphics.
- Control AI.
- Process user input.
"""
from engine.interfaces.game_result import GameResult
from games.tic_tac_toe.constants import (
    BOARD_ROWS,
    BOARD_COLUMNS,
    EMPTY,
    NO_WINNER,
)


class TicTacToeRules:
    """
    Rule engine for Tic-Tac-Toe.

    This class only evaluates the current board state.
    """

    @staticmethod
    def check_winner(board):
        """
        Determine whether a player has won.

        Args:
            board (TicTacToeBoard): Board to evaluate.

        Returns:
            int:
                PLAYER_X
                PLAYER_O
                NO_WINNER
        """

        # -----------------------------
        # Check all rows
        # -----------------------------
        for row in range(BOARD_ROWS):

            first = board.get_cell(row, 0)

            if first == EMPTY:
                continue

            winner = True

            for column in range(1, BOARD_COLUMNS):
                if board.get_cell(row, column) != first:
                    winner = False
                    break

            if winner:
                return first

        # -----------------------------
        # Check all columns
        # -----------------------------
        for column in range(BOARD_COLUMNS):

            first = board.get_cell(0, column)

            if first == EMPTY:
                continue

            winner = True

            for row in range(1, BOARD_ROWS):
                if board.get_cell(row, column) != first:
                    winner = False
                    break

            if winner:
                return first

        # -----------------------------
        # Check main diagonal
        # -----------------------------
        first = board.get_cell(0, 0)

        if first != EMPTY:

            winner = True

            for index in range(1, BOARD_ROWS):
                if board.get_cell(index, index) != first:
                    winner = False
                    break

            if winner:
                return first

        # -----------------------------
        # Check anti-diagonal
        # -----------------------------
        first = board.get_cell(0, BOARD_COLUMNS - 1)

        if first != EMPTY:

            winner = True

            for index in range(1, BOARD_ROWS):
                if board.get_cell(index, BOARD_COLUMNS - 1 - index) != first:
                    winner = False
                    break

            if winner:
                return first

        return NO_WINNER

    @staticmethod
    def get_winning_cells(board):
        """
        Return the coordinates of the winning line.

        Returns
        -------
        list[tuple[int, int]]

        Empty list if there is no winner.
        """

        # -----------------------------
        # Rows
        # -----------------------------

        for row in range(BOARD_ROWS):

            first = board.get_cell(row, 0)

            if first == EMPTY:
                continue

            winner = True

            for column in range(1, BOARD_COLUMNS):

                if board.get_cell(row, column) != first:
                    winner = False
                    break

            if winner:

                return [
                    (row, column)
                    for column in range(BOARD_COLUMNS)
                ]

        # -----------------------------
        # Columns
        # -----------------------------

        for column in range(BOARD_COLUMNS):

            first = board.get_cell(0, column)

            if first == EMPTY:
                continue

            winner = True

            for row in range(1, BOARD_ROWS):

                if board.get_cell(row, column) != first:
                    winner = False
                    break

            if winner:

                return [
                    (row, column)
                    for row in range(BOARD_ROWS)
                ]

        # -----------------------------
        # Main diagonal
        # -----------------------------

        first = board.get_cell(0, 0)

        if first != EMPTY:

            winner = True

            for index in range(1, BOARD_ROWS):

                if board.get_cell(index, index) != first:
                    winner = False
                    break

            if winner:

                return [
                    (index, index)
                    for index in range(BOARD_ROWS)
                ]

        # -----------------------------
        # Anti-diagonal
        # -----------------------------

        first = board.get_cell(0, BOARD_COLUMNS - 1)

        if first != EMPTY:

            winner = True

            for index in range(1, BOARD_ROWS):

                if (
                    board.get_cell(
                        index,
                        BOARD_COLUMNS - 1 - index,
                    )
                    != first
                ):
                    winner = False
                    break

            if winner:

                return [
                    (
                        index,
                        BOARD_COLUMNS - 1 - index,
                    )
                    for index in range(BOARD_ROWS)
                ]

        return []
    @staticmethod
    def is_draw(board):
        """
        Determine whether the game is a draw.

        Args:
            board (TicTacToeBoard)

        Returns:
            bool
        """

        return (
            TicTacToeRules.check_winner(board) == NO_WINNER
            and
            board.is_board_full()
        )

    @staticmethod
    def is_game_over(board):
        """
        Determine whether the game has ended.

        Args:
            board (TicTacToeBoard)

        Returns:
            bool
        """

        if TicTacToeRules.check_winner(board) != NO_WINNER:
            return True

        if board.is_board_full():
            return True

        return False
    @staticmethod
    def evaluate_game(board):
        """
        Evaluate the complete game state.

        Returns
        -------
        GameResult
            Universal result object describing the current match.
        """

        result = GameResult()

        winner = TicTacToeRules.check_winner(board)

        if winner != NO_WINNER:

            result.winner = winner
            result.game_over = True

            # Winning cells will be added
            # in Step 8.2.
            result.winning_cells = TicTacToeRules.get_winning_cells(board)

            return result

        if board.is_board_full():

            result.draw = True
            result.game_over = True

            return result

        return result