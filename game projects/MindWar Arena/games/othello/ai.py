# games/othello/ai.py
import random
from engine.interfaces.ai_interface import AIInterface
from games.othello.constants import (PLAYER_BLACK,PLAYER_WHITE,)
from games.othello.rules import OthelloRules
class OthelloAI(AIInterface):
    def __init__(self):
        self.initialized = False
    def initialize(self):
        self.initialized = True
    def reset(self):
        self.initialized = False
    def select_action(self, game_state):
        if not self.initialized:
            return None
        if not game_state:
            return None
        board_state = game_state.get("board")
        if board_state is None:
            return None
        player = game_state.get("current_player")
        if player not in (PLAYER_BLACK,PLAYER_WHITE,):
            return None
        legal_moves = self._get_legal_moves(board_state,player,)
        if not legal_moves:
            return None
        return random.choice(legal_moves)
    def _get_legal_moves(self, board_state, player):
        from games.othello.board import OthelloBoard
        board = OthelloBoard()
        board._board = [list(row) for row in board_state]
        return OthelloRules.get_legal_moves(board,player,)
    def get_action(self, game):
        return self.select_action(game.get_state())
    def learn(self,state,action,reward,next_state,):
        pass