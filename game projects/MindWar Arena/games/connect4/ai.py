import random

from engine.interfaces.ai_interface import AIInterface


class Connect4AI(AIInterface):
    def __init__(self):
        self.initialized = False

    def initialize(self):
        self.initialized = True

    def select_action(self, game_state):
        board = game_state["board"]

        legal_moves = []

        columns = len(board[0])

        for column in range(columns):
            if board[0][column] == 0:
                legal_moves.append(column)

        if not legal_moves:
            return None

        return random.choice(legal_moves)

    def learn(self, state, action, reward, next_state):
        pass

    def reset(self):
        self.initialized = False

    def get_action(self, game):
        return self.select_action(game.get_state())