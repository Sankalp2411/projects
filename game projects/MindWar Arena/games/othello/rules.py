# games/othello/rules.py
from engine.interfaces.game_result import GameResult
from games.othello.constants import (BOARD_ROWS,BOARD_COLUMNS,EMPTY,PLAYER_BLACK,PLAYER_WHITE,)
class OthelloRules:
    _DIRECTIONS = ((-1, -1),(-1, 0),(-1, 1),(0, -1),(0, 1),(1, -1),(1, 0),(1, 1),)
    @staticmethod
    def get_opponent(player):
        if player == PLAYER_BLACK:
            return PLAYER_WHITE
        if player == PLAYER_WHITE:
            return PLAYER_BLACK
        raise ValueError(f"Invalid player: {player}")
    @classmethod
    def is_valid_move(cls, board, row, column, player):
        if player not in (PLAYER_BLACK, PLAYER_WHITE):
            return False
        if not board.is_valid_position(row, column):
            return False
        if not board.is_cell_empty(row, column):
            return False
        return bool(cls.get_flips(board,row,column,player,))
    @classmethod
    def get_flips(cls, board, row, column, player):
        if player not in (PLAYER_BLACK, PLAYER_WHITE):
            return []
        if not board.is_valid_position(row, column):
            return []
        if not board.is_cell_empty(row, column):
            return []
        opponent = cls.get_opponent(player)
        flips = []
        for direction_row, direction_column in cls._DIRECTIONS:
            direction_flips = cls._get_direction_flips(board,row,column,player,opponent,direction_row,direction_column,)
            flips.extend(direction_flips)
        return flips
    @classmethod
    def _get_direction_flips(cls,board,row,column,player,opponent,direction_row,direction_column,):
        current_row = row + direction_row
        current_column = column + direction_column
        potential_flips = []
        while board.is_valid_position(current_row,current_column,):
            cell = board.get_cell(current_row,current_column,)
            if cell == opponent:
                potential_flips.append((current_row, current_column))
            elif cell == player:
                if potential_flips:
                    return potential_flips
                return []
            else:
                return []
            current_row += direction_row
            current_column += direction_column
        return []
    @classmethod
    def get_legal_moves(cls, board, player):
        legal_moves = []
        if player not in (PLAYER_BLACK, PLAYER_WHITE):
            return legal_moves
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                if cls.is_valid_move(board,row,column,player,):
                    legal_moves.append((row, column))
        return legal_moves
    @classmethod
    def apply_move(cls, board, row, column, player):
        if not cls.is_valid_move(board,row,column,player,):
            return False
        flips = cls.get_flips(board,row,column,player,)
        board.set_cell(row,column,player,)
        for flip_row, flip_column in flips:
            board.set_cell(flip_row,flip_column,player,)
        return True
    @classmethod
    def can_player_move(cls, board, player):
        return bool(cls.get_legal_moves(board,player,))
    @classmethod
    def is_game_over(cls, board):
        if board.is_board_full():
            return True
        return (not cls.can_player_move(board,PLAYER_BLACK,) and not cls.can_player_move( board,PLAYER_WHITE,))
    @staticmethod
    def get_winner(board):
        black_count = board.count_stones(PLAYER_BLACK)
        white_count = board.count_stones(PLAYER_WHITE)
        if black_count > white_count:
            return PLAYER_BLACK
        if white_count > black_count:
            return PLAYER_WHITE
        return None
    @classmethod
    def is_draw(cls, board):
        if not cls.is_game_over(board):
            return False
        black_count = board.count_stones(PLAYER_BLACK)
        white_count = board.count_stones(PLAYER_WHITE)
        return black_count == white_count
    @classmethod
    def evaluate_game(cls, board):
        result = GameResult()
        if not cls.is_game_over(board):
            return result
        result.game_over = True
        black_count = board.count_stones(PLAYER_BLACK)
        white_count = board.count_stones(PLAYER_WHITE)
        if black_count > white_count:
            result.winner = PLAYER_BLACK
        elif white_count > black_count:
            result.winner = PLAYER_WHITE
        else:
            result.draw = True
        return result