"""
MindWar Arena
Phase 2 - Tic-Tac-Toe

ai.py

Random AI implementation for Tic-Tac-Toe.

Responsibilities:
- Select a random legal move.
- Implement AIInterface.

This module does NOT:
- Modify the game.
- Place pieces.
- Check rules.
- Render graphics.
"""

import random

from engine.interfaces.ai_interface import AIInterface


class TicTacToeAI(AIInterface):
    """
    Random AI for Tic-Tac-Toe.
    """

    def __init__(self):
        self.initialized = False

    def initialize(self):
        """
        Initialize the AI.
        """
        self.initialized = True

    def select_action(self, game_state):
        """
        Select a random legal move.

        Args:
            game_state (dict):
                Dictionary returned by
                TicTacToeGame.get_state()

        Returns:
            tuple[int, int] | None
                (row, column) if a move exists.
                None if no legal moves remain.
        """

        board = game_state["board"]

        legal_moves = []

        for row in range(len(board)):
            for column in range(len(board[row])):
                if board[row][column] == 0:
                    legal_moves.append((row, column))

        if not legal_moves:
            return None

        return random.choice(legal_moves)

    def learn(self, state, action, reward, next_state):
        """
        Random AI does not learn.
        """
        pass

    def reset(self):
        """
        Reset AI state.
        """
        self.initialized = False