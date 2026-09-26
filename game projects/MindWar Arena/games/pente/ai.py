# games/pente/ai.py
import random
from engine.interfaces.ai_interface import AIInterface
class PenteAI(AIInterface):
    def __init__(self):
        self.initialized = False
    def initialize(self):
        self.initialized = True
    def reset(self):
        self.initialized = False
    def select_action(self, game_state):
        if not self.initialized:
            return None
        board = game_state.get("board")
        if board is None:
            return None
        legal_moves = []
        for row in range(len(board)):
            for column in range(len(board[row])):
                if board[row][column] == 0:
                    legal_moves.append((row, column))
        if not legal_moves:
            return None
        return random.choice(legal_moves)
    def get_action(self, game):
        return self.select_action(game.get_state())
    def learn(self,state,action,reward,next_state,):
        pass