# games/checkers/rules.py
from engine.interfaces.game_result import GameResult
from games.checkers.constants import (BLACK_KING,BLACK_MAN,BOARD_COLUMNS,BOARD_ROWS,EMPTY,FORWARD_BLACK,FORWARD_WHITE,PLAYER_BLACK,PLAYER_WHITE,WHITE_KING,WHITE_MAN,)
class CheckersRules:
    _DIAGONAL_DIRECTIONS = ((-1, -1),(-1, 1),(1, -1),(1, 1),)
    @staticmethod
    def get_opponent(player):
        if player == PLAYER_BLACK:
            return PLAYER_WHITE
        if player == PLAYER_WHITE:
            return PLAYER_BLACK
        raise ValueError(f"Invalid player: {player}")
    @staticmethod
    def is_player_piece(piece, player):
        if player == PLAYER_BLACK:
            return piece in (BLACK_MAN, BLACK_KING)
        if player == PLAYER_WHITE:
            return piece in (WHITE_MAN, WHITE_KING)
        return False
    @staticmethod
    def is_man(piece):
        return piece in (BLACK_MAN, WHITE_MAN)
    @staticmethod
    def is_king(piece):
        return piece in (BLACK_KING, WHITE_KING)
    @classmethod
    def get_move_directions(cls, piece, player):
        if not cls.is_player_piece(piece, player):
            return ()
        if cls.is_king(piece):
            return cls._DIAGONAL_DIRECTIONS
        if player == PLAYER_BLACK:
            return ((FORWARD_BLACK, -1),(FORWARD_BLACK, 1),)
        return ((FORWARD_WHITE, -1),(FORWARD_WHITE, 1),)
    @classmethod
    def get_simple_moves(cls, board, row, column):
        if not board.is_valid_position(row, column):
            return []
        piece = board.get_cell(row, column)
        if piece == EMPTY:
            return []
        if not cls.is_king(piece):
            if piece == BLACK_MAN:
                player = PLAYER_BLACK
            elif piece == WHITE_MAN:
                player = PLAYER_WHITE
            else:
                return []
        else:
            if piece == BLACK_KING:
                player = PLAYER_BLACK
            else:
                player = PLAYER_WHITE
        moves = []
        for direction_row, direction_column in cls.get_move_directions(piece,player,):
            destination_row = row + direction_row
            destination_column = column + direction_column
            if not board.is_valid_position(destination_row,destination_column,):
                continue
            if not board.is_playable_square(destination_row,destination_column,):
                continue
            if board.is_cell_empty(destination_row,destination_column,):
                moves.append((row,column,destination_row,destination_column,))
        return moves
    @classmethod
    def get_capture_moves(cls, board, row, column):
        if not board.is_valid_position(row, column):
            return []
        piece = board.get_cell(row, column)
        if piece == EMPTY:
            return []
        if piece == BLACK_MAN or piece == BLACK_KING:
            player = PLAYER_BLACK
        elif piece == WHITE_MAN or piece == WHITE_KING:
            player = PLAYER_WHITE
        else:
            return []
        opponent = cls.get_opponent(player)
        capture_moves = []
        for direction_row, direction_column in cls.get_move_directions(piece,player,):
            jumped_row = row + direction_row
            jumped_column = column + direction_column
            landing_row = row + (direction_row * 2)
            landing_column = column + (direction_column * 2)
            if not board.is_valid_position(jumped_row,jumped_column,):
                continue
            if not board.is_valid_position(landing_row,landing_column,):
                continue
            jumped_piece = board.get_cell(jumped_row,jumped_column,)
            if not cls.is_player_piece(jumped_piece,opponent,):
                continue
            if not board.is_cell_empty(landing_row,landing_column,):
                continue
            if not board.is_playable_square(landing_row,landing_column,):
                continue
            capture_moves.append((row,column,landing_row,landing_column,))
        return capture_moves
    @classmethod
    def get_piece_moves(cls, board, row, column, player):
        if not board.is_valid_position(row, column):
            return []
        piece = board.get_cell(row, column)
        if not cls.is_player_piece(piece, player):
            return []
        capture_moves = cls.get_capture_moves(board,row,column,)
        if capture_moves:
            return capture_moves
        return cls.get_simple_moves(board,row,column,)
    @classmethod
    def get_all_capture_moves(cls, board, player):
        capture_moves = []
        for row, column in board.get_piece_positions(player):
            capture_moves.extend(cls.get_capture_moves(board,row,column,))
        return capture_moves
    @classmethod
    def get_all_simple_moves(cls, board, player):
        simple_moves = []
        for row, column in board.get_piece_positions(player):
            simple_moves.extend(cls.get_simple_moves(board,row,column,))
        return simple_moves
    @classmethod
    def get_legal_moves(cls, board, player):
        if player not in (PLAYER_BLACK, PLAYER_WHITE):
            return []
        capture_moves = cls.get_all_capture_moves(board,player,)
        if capture_moves:
            return capture_moves
        return cls.get_all_simple_moves(board,player,)
    @classmethod
    def has_capture(cls, board, player):
        return bool(cls.get_all_capture_moves(board,player,))
    @classmethod
    def has_any_legal_move(cls, board, player):
        return bool(cls.get_legal_moves(board,player,))
    @classmethod
    def is_valid_move(cls, board, move, player):
        if not isinstance(move, tuple):
            return False
        if len(move) != 4:
            return False
        if player not in (PLAYER_BLACK, PLAYER_WHITE):
            return False
        try:
            from_row, from_column, to_row, to_column = move
        except ValueError:
            return False
        legal_moves = cls.get_legal_moves(board,player,)
        return move in legal_moves
    @classmethod
    def is_capture_move(cls, move):
        if not isinstance(move, tuple):
            return False
        if len(move) != 4:
            return False
        from_row, from_column, to_row, to_column = move
        return abs(to_row - from_row) == 2 and abs(to_column - from_column) == 2
    @classmethod
    def get_captured_position(cls, move):
        if not cls.is_capture_move(move):
            return None
        from_row, from_column, to_row, to_column = move
        captured_row = (from_row + to_row) // 2
        captured_column = (from_column + to_column) // 2
        return captured_row, captured_column
    @classmethod
    def should_promote(cls, piece, row):
        if piece == BLACK_MAN:
            return row == BOARD_ROWS - 1
        if piece == WHITE_MAN:
            return row == 0
        return False
    @staticmethod
    def promote_piece(piece):
        if piece == BLACK_MAN:
            return BLACK_KING
        if piece == WHITE_MAN:
            return WHITE_KING
        return piece
    @classmethod
    def apply_move(cls, board, move, player):
        if not cls.is_valid_move(board,move,player,):
            return False
        from_row, from_column, to_row, to_column = move
        piece = board.get_cell(from_row,from_column,)
        board.set_cell(from_row,from_column,EMPTY,)
        if cls.is_capture_move(move):
            captured_position = cls.get_captured_position(move)
            if captured_position is not None:
                captured_row, captured_column = captured_position
                board.set_cell(captured_row,captured_column,EMPTY,)
        if cls.should_promote(piece, to_row):
            piece = cls.promote_piece(piece)
        board.set_cell(to_row,to_column,piece,)
        return True
    @classmethod
    def get_winner(cls, board):
        black_count = board.count_pieces(PLAYER_BLACK)
        white_count = board.count_pieces(PLAYER_WHITE)
        if black_count == 0 and white_count == 0:
            return None
        if black_count == 0:
            return PLAYER_WHITE
        if white_count == 0:
            return PLAYER_BLACK
        if not cls.has_any_legal_move(board,PLAYER_BLACK,):
            return PLAYER_WHITE
        if not cls.has_any_legal_move(board,PLAYER_WHITE,):
            return PLAYER_BLACK
        return None
    @classmethod
    def is_game_over(cls, board):
        black_count = board.count_pieces(PLAYER_BLACK)
        white_count = board.count_pieces(PLAYER_WHITE)
        if black_count == 0 or white_count == 0:
            return True
        return (
            not cls.has_any_legal_move(board,PLAYER_BLACK,) or not cls.has_any_legal_move(board,PLAYER_WHITE,))
    @classmethod
    def is_draw(cls, board):
        return False
    @classmethod
    def evaluate_game(cls, board):
        result = GameResult()
        if not cls.is_game_over(board):
            return result
        result.game_over = True
        winner = cls.get_winner(board)
        if winner is not None:
            result.winner = winner
        else:
            result.draw = True
        return result