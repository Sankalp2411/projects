# games/chess/ai.py
import random
from engine.interfaces.ai_interface import AIInterface
from games.chess.board import ChessBoard
from games.chess.constants import (AI_RANDOM,KING_VALUE,PLAYER_BLACK,PLAYER_WHITE,)
from games.chess.rules import ChessRules
class ChessAI(AIInterface):
    def __init__(self, player):
        if player not in (PLAYER_WHITE,PLAYER_BLACK,):
            raise ValueError(f"Invalid player: {player}")
        self.player = player
        self.difficulty = AI_RANDOM
        self.search_depth = 1
    def initialize(self):
        pass
    def reset(self):
        pass
    def get_action(self, game):
        if game is None:
            return None
        if game.is_game_over():
            return None
        current_player = (game.get_current_player())
        if current_player != self.player:
            self.set_player(current_player)
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return None
        game_state = game.get_state()
        return self.select_action(game_state)
    def select_action(self, game_state):
        if not isinstance(game_state,dict,):
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
        selected_move = random.choice(valid_moves)
        return tuple(selected_move)
    @staticmethod
    def simulate_move(board,move,player,en_passant_target=None,castling_rights=None,):
        if board is None:
            return None
        if player not in (PLAYER_WHITE,PLAYER_BLACK,):
            return None
        if not ChessAI._is_valid_move_format(move):
            return None
        simulated_board = board.copy()
        if not ChessRules.apply_legal_move(simulated_board,move,player,en_passant_target,castling_rights,):
            return None
        return simulated_board
    def select_minimax_move(self,board,player=None,depth=None,en_passant_target=None,castling_rights=None,):
        if board is None:
            return None
        if player is None:
            player = self.player
        if player not in (PLAYER_WHITE,PLAYER_BLACK,):
            return None
        if depth is None:
            depth = self.search_depth
        if not isinstance(depth,int,):
            return None
        if depth < 1:
            return None
        legal_moves = (ChessRules.get_legal_moves(board,player,en_passant_target,castling_rights,))
        if not legal_moves:
            return None
        best_move = None
        if player == PLAYER_WHITE:
            best_score = float("-inf")
            for move in legal_moves:
                simulated_board = (
                    self.simulate_move(board,move,player,en_passant_target,castling_rights,))
                if simulated_board is None:
                    continue
                score = self.minimax(simulated_board,depth - 1,PLAYER_BLACK,None,castling_rights,)
                if (best_move is None or score > best_score):
                    best_score = score
                    best_move = tuple(move)
        else:
            best_score = float("inf")
            for move in legal_moves:
                simulated_board = (self.simulate_move(board,move,player,en_passant_target,castling_rights,))
                if simulated_board is None:
                    continue
                score = self.minimax(simulated_board,depth - 1,PLAYER_WHITE,None,castling_rights,)
                if (best_move is None or score < best_score):
                    best_score = score
                    best_move = tuple(move)
        return best_move
    def minimax(self,board,depth,player,en_passant_target=None,castling_rights=None,):
        if board is None:
            return 0
        if player not in (PLAYER_WHITE,PLAYER_BLACK,):
            return 0
        if not isinstance(depth,int,):
            return 0
        if depth < 0:
            return 0
        legal_moves = (
            ChessRules.get_legal_moves(board,player,en_passant_target,castling_rights,))
        if not legal_moves:
            if ChessRules.is_in_check(board,player,):
                return self.get_checkmate_score(player,depth,)
            return 0
        if depth == 0:
            return ChessRules.evaluate_material(board)
        if player == PLAYER_WHITE:
            best_score = float("-inf")
            for move in legal_moves:
                simulated_board = (self.simulate_move(board,move,player,en_passant_target,castling_rights,))
                if simulated_board is None:
                    continue
                score = self.minimax(simulated_board,depth - 1,PLAYER_BLACK,None,castling_rights,)
                if score > best_score:
                    best_score = score
            if best_score == float("-inf"):
                return ChessRules.evaluate_material(board)
            return best_score
        best_score = float("inf")
        for move in legal_moves:
            simulated_board = (self.simulate_move(board,move,player,en_passant_target,castling_rights,))
            if simulated_board is None:
                continue
            score = self.minimax(simulated_board,depth - 1,PLAYER_WHITE,None,castling_rights,)
            if score < best_score:
                best_score = score
        if best_score == float("inf"):
            return ChessRules.evaluate_material(board)
        return best_score
    @staticmethod
    def get_checkmate_score(player,depth,):
        if player not in (PLAYER_WHITE,PLAYER_BLACK,):
            return 0
        if not isinstance(depth,int,):
            return 0
        if depth < 0:
            return 0
        if player == PLAYER_WHITE:
            return -(KING_VALUE + depth)
        return (KING_VALUE + depth)
    def learn(self,state,action,reward,next_state,):
        pass
    def set_player(self, player):
        if player not in (PLAYER_WHITE,PLAYER_BLACK,):
            raise ValueError(f"Invalid player: {player}")
        self.player = player
    def set_difficulty(self, difficulty):
        if not isinstance(difficulty,str,):
            raise ValueError("Difficulty must be a string.")
        self.difficulty = difficulty
    def get_player(self):
        return self.player
    def get_difficulty(self):
        return self.difficulty
    def set_search_depth(self, depth):
        if not isinstance(depth,int,):
            raise ValueError("Search depth must be an integer.")
        if depth < 1:
            raise ValueError("Search depth must be at least 1.")
        self.search_depth = depth
    def get_search_depth(self):
        return self.search_depth
    @staticmethod
    def _is_valid_move_format(move):
        if not isinstance(move,(tuple, list),):
            return False
        if len(move) != 4:
            return False
        return all(isinstance(value,int,)for value in move)
    @staticmethod
    def get_random_move(board,player,):
        legal_moves = (ChessRules.get_all_piece_moves(board,player,))
        if not legal_moves:
            return None
        return tuple(random.choice(legal_moves))