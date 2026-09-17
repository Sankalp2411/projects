#games/nine_mens_morris/rules.py
from engine.interfaces.game_result import GameResult
from games.nine_mens_morris.constants import (EMPTY,PLAYER_BLACK,PLAYER_WHITE,NO_WINNER,PHASE_PLACEMENT,PHASE_MOVEMENT,PHASE_FLYING,PIECES_PER_PLAYER,)
class NineMensMorrisRules:
    _ADJACENCY = {0: (1, 9),1: (0, 2, 4),2: (1, 14),3: (4, 10),4: (1, 3, 5, 7),5: (4, 13),6: (7, 11),7: (4, 6, 8),8: (7, 12),9: (0, 10, 21),10: (3, 9, 11, 18),11: (6, 10, 15),12: (8, 13, 17),13: (5, 12, 14, 20),14: (2, 13, 23),15: (11, 16),16: (15, 17, 19),17: (12, 16),18: (10, 19),19: (16, 18, 20, 22),20: (13, 19),21: (9, 22),22: (19, 21, 23),23: (14, 22),}
    _MILLS = ((0, 1, 2),(3, 4, 5),(6, 7, 8),(9, 10, 11),(12, 13, 14),(15, 16, 17),(18, 19, 20),(21, 22, 23),(0, 9, 21),(3, 10, 18),(6, 11, 15),(1, 4, 7),(16, 19, 22),(2, 14, 23),(5, 13, 20),(8, 12, 17),)
    @staticmethod
    def get_opponent(player):
        if player == PLAYER_BLACK:
            return PLAYER_WHITE
        if player == PLAYER_WHITE:
            return PLAYER_BLACK
        return EMPTY
    @staticmethod
    def get_adjacent_positions(position):
        return NineMensMorrisRules._ADJACENCY.get(position, ())
    @staticmethod
    def are_adjacent(source, destination):
        if source not in NineMensMorrisRules._ADJACENCY:
            return False
        return destination in NineMensMorrisRules._ADJACENCY[source]
    @staticmethod
    def get_mills_for_position(position):
        mills = []
        for mill in NineMensMorrisRules._MILLS:
            if position in mill:
                mills.append(mill)
        return mills
    @staticmethod
    def is_mill(board, position, player=None):
        if not board.is_valid_position(position):
            return False
        if player is None:
            player = board.get_position(position)
        if player == EMPTY:
            return False
        for mill in NineMensMorrisRules.get_mills_for_position(position):
            if all(board.get_position(cell) == player for cell in mill):
                return True
        return False
    @staticmethod
    def get_mill_cells(board, player):
        mills = []
        if player not in (PLAYER_BLACK, PLAYER_WHITE):
            return mills
        for mill in NineMensMorrisRules._MILLS:
            if all(board.get_position(position) == player for position in mill):
                mills.append(mill)
        return mills
    @staticmethod
    def get_winning_cells(board, player):
        mills = NineMensMorrisRules.get_mill_cells(board, player)
        if not mills:
            return []
        return list(mills[0])
    @staticmethod
    def can_fly(board, player):
        return board.count_pieces(player) == 3
    @staticmethod
    def get_phase(board, pieces_placed):
        if pieces_placed < PIECES_PER_PLAYER * 2:
            return PHASE_PLACEMENT
        return PHASE_MOVEMENT
    @staticmethod
    def get_legal_destinations(board, source, player):
        if not board.is_valid_position(source):
            return []
        if board.get_position(source) != player:
            return []
        destinations = []
        if NineMensMorrisRules.can_fly(board, player):
            for position in board.get_available_positions():
                destinations.append(position)
            return destinations
        for position in NineMensMorrisRules.get_adjacent_positions(source):
            if board.is_position_empty(position):
                destinations.append(position)
        return destinations
    @staticmethod
    def get_legal_moves(board, player):
        moves = []
        player_positions = board.get_player_positions(player)
        for source in player_positions:
            destinations = NineMensMorrisRules.get_legal_destinations(board,source,player,)
            for destination in destinations:
                moves.append((source, destination))
        return moves
    @staticmethod
    def has_legal_move(board, player):
        return len(NineMensMorrisRules.get_legal_moves(board, player)) > 0
    @staticmethod
    def can_remove_piece(board, position, player):
        if not board.is_valid_position(position):
            return False
        opponent = NineMensMorrisRules.get_opponent(player)
        if opponent == EMPTY:
            return False
        if board.get_position(position) != opponent:
            return False
        opponent_positions = board.get_player_positions(opponent)
        if NineMensMorrisRules.is_mill(board,position,opponent,):
            non_mill_positions = []
            for opponent_position in opponent_positions:
                if not NineMensMorrisRules.is_mill(board,opponent_position,opponent,):
                    non_mill_positions.append(opponent_position)
            if non_mill_positions:
                return False
        return True
    @staticmethod
    def get_removable_pieces(board, player):
        opponent = NineMensMorrisRules.get_opponent(player)
        if opponent == EMPTY:
            return []
        opponent_positions = board.get_player_positions(opponent)
        non_mill_positions = [ position for position in opponent_positions if not NineMensMorrisRules.is_mill(board,position,opponent,)]
        if non_mill_positions:
            return non_mill_positions
        return opponent_positions
    @staticmethod
    def is_winner(board, player):
        opponent = NineMensMorrisRules.get_opponent(player)
        if opponent == EMPTY:
            return False
        opponent_piece_count = board.count_pieces(opponent)
        if opponent_piece_count < 3:
            return True
        if not NineMensMorrisRules.has_legal_move(board, opponent):
            return True
        return False
    @staticmethod
    def is_draw(board, player):
        if board.is_board_full():
            return True
        return False
    @staticmethod
    def evaluate_game(board, current_player):
        result = GameResult()
        opponent = NineMensMorrisRules.get_opponent(current_player)
        if opponent != EMPTY:
            if NineMensMorrisRules.is_winner(board, current_player):
                result.winner = current_player
                result.game_over = True
                result.winning_cells = (
                    NineMensMorrisRules.get_winning_cells(board,current_player,))
                return result
        if current_player != EMPTY:
            if NineMensMorrisRules.is_winner(board, opponent):
                result.winner = opponent
                result.game_over = True
                result.winning_cells = (NineMensMorrisRules.get_winning_cells(board,opponent,))
                return result
        if NineMensMorrisRules.is_draw(board,current_player,):
            result.draw = True
            result.game_over = True
            return result
        return result