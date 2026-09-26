#games/go/ai.py
import random
from engine.interfaces.ai_interface import AIInterface
from games.go.constants import (ACTION_PASS,PLAYER_BLACK,PLAYER_WHITE,)
from games.go.rules import GoRules
class GoAI(AIInterface):
    def __init__(self, player):
        self.player = player
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
        current_player = game_state.get("current_player")
        if current_player != self.player:
            return None
        previous_board_state = game_state.get("previous_board")
        from games.go.board import GoBoard
        board = GoBoard()
        board.set_board_state(board_state)
        previous_board = None
        if previous_board_state is not None:
            previous_board = GoBoard()
            previous_board.set_board_state(previous_board_state)
        legal_moves = GoRules.get_legal_moves(board,self.player,previous_board,)
        if not legal_moves:
            return ACTION_PASS
        return random.choice(legal_moves)
    def get_action(self, game):
        return self.select_action(game.get_state())
    def learn(self,state,action,reward,next_state,):
        pass