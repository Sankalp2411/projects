# games/checkers/ai.py
import random
from engine.interfaces.ai_interface import AIInterface
from games.checkers.constants import (AI_RANDOM,PLAYER_BLACK,PLAYER_WHITE,)
from games.checkers.rules import CheckersRules
class CheckersAI(AIInterface):
    def __init__(self, player):
        if player not in (PLAYER_BLACK,PLAYER_WHITE,):
            raise ValueError(f"Invalid player: {player}")
        self.player = player
        self.difficulty = AI_RANDOM
    def initialize(self):
        pass
    def get_action(self, game):
        if game is None:
            return None
        if game.is_game_over():
            return None
        current_player = game.get_current_player()
        if current_player != self.player:
            self.set_player(current_player)
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return None
        game_state = game.get_state()
        return self.select_action(game_state)
    def select_action(self, game_state):
        if not isinstance(game_state, dict):
            return None
        legal_moves = game_state.get("legal_moves",[],)
        if not legal_moves:
            return None
        valid_moves = []
        for move in legal_moves:
            if self._is_valid_move_format(move):
                valid_moves.append(tuple(move))
        if not valid_moves:
            return None
        return random.choice(valid_moves)
    def learn(self,state,action,reward,next_state,):
        pass
    def reset(self):
        pass
    def set_player(self, player):
        if player not in (PLAYER_BLACK,PLAYER_WHITE,):
            raise ValueError(f"Invalid player: {player}")
        self.player = player
    def set_difficulty(self, difficulty):
        if not isinstance(difficulty,str,):
            raise ValueError("Difficulty must be a string.")
        self.difficulty = difficulty
    @staticmethod
    def _is_valid_move_format(move):
        if not isinstance(move,(tuple, list),):
            return False
        if len(move) != 4:
            return False
        return all(isinstance(value,int,) for value in move)
    @staticmethod
    def get_random_move(board, player):
        legal_moves = CheckersRules.get_legal_moves(board,player,)
        if not legal_moves:
            return None
        return random.choice(legal_moves)