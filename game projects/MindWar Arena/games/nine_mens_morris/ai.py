#games/nine_mens_morris/ai.py
import random
from engine.interfaces.ai_interface import AIInterface
from games.nine_mens_morris.constants import (PLAYER_BLACK,PLAYER_WHITE,PHASE_PLACEMENT,PHASE_MOVEMENT,)
from games.nine_mens_morris.rules import NineMensMorrisRules
class NineMensMorrisAI(AIInterface):
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
        player = game_state.get("current_player")
        if player not in (PLAYER_BLACK, PLAYER_WHITE):
            return None
        phase = game_state.get("phase")
        if phase == PHASE_PLACEMENT:
            available_positions = []
            for position in range(len(board)):
                if board[position] == 0:
                    available_positions.append(position)
            if not available_positions:
                return None
            return random.choice(available_positions)
        legal_moves = []
        for source in range(len(board)):
            if board[source] != player:
                continue
            destinations = []
            if game_state.get("flying"):
                for destination in range(len(board)):
                    if board[destination] == 0:
                        destinations.append(destination)
            else:
                destinations = (NineMensMorrisRules.get_adjacent_positions(source))
                destinations = [destination for destination in destinations if board[destination] == 0]
            for destination in destinations:
                legal_moves.append((source, destination))
        if not legal_moves:
            return None
        return random.choice(legal_moves)
    def get_action(self, game):
        return self.select_action(game.get_state())
    def learn(self,state,action,reward,next_state,):
        pass