# games/chess/rules.py
from engine.interfaces.game_result import GameResult
from games.chess.constants import (BLACK_BISHOP,BLACK_KING,BLACK_KNIGHT,BLACK_PAWN,BLACK_QUEEN,BLACK_ROOK,BLACK_PAWN_DIRECTION,BISHOP_DIRECTIONS,BOARD_COLUMNS,BOARD_ROWS,CASTLING_KINGSIDE,CASTLING_QUEENSIDE,EMPTY,KING_DIRECTIONS,KING_MOVE_DISTANCE,KNIGHT_DIRECTIONS,KNIGHT_MOVE_DISTANCE,PLAYER_BLACK,PLAYER_WHITE,PROMOTION_BISHOP,PROMOTION_KNIGHT,PROMOTION_NONE,PROMOTION_QUEEN,PROMOTION_ROOK,QUEEN_DIRECTIONS,ROOK_DIRECTIONS,WHITE_BISHOP,WHITE_KING,WHITE_KNIGHT,WHITE_PAWN,WHITE_PAWN_DIRECTION,WHITE_QUEEN,WHITE_ROOK,WHITE_PROMOTION_ROW,BLACK_PROMOTION_ROW,)
class ChessRules:
    @staticmethod
    def get_opponent(player):
        if player == PLAYER_WHITE:
            return PLAYER_BLACK
        if player == PLAYER_BLACK:
            return PLAYER_WHITE
        return None
    @staticmethod
    def is_valid_player(player):
        return player in (PLAYER_WHITE,PLAYER_BLACK,)
    @staticmethod
    def is_white_piece(piece):
        return piece in (WHITE_PAWN,WHITE_KNIGHT,WHITE_BISHOP,WHITE_ROOK,WHITE_QUEEN,WHITE_KING,)
    @staticmethod
    def is_black_piece(piece):
        return piece in (BLACK_PAWN,BLACK_KNIGHT,BLACK_BISHOP,BLACK_ROOK,BLACK_QUEEN,BLACK_KING,)
    @staticmethod
    def is_pawn(piece):
        return piece in (WHITE_PAWN,BLACK_PAWN,)
    @staticmethod
    def is_knight(piece):
        return piece in (WHITE_KNIGHT,BLACK_KNIGHT,)
    @staticmethod
    def is_bishop(piece):
        return piece in (WHITE_BISHOP,BLACK_BISHOP,)
    @staticmethod
    def is_rook(piece):
        return piece in (WHITE_ROOK,BLACK_ROOK,)
    @staticmethod
    def is_queen(piece):
        return piece in (WHITE_QUEEN,BLACK_QUEEN,)
    @staticmethod
    def is_king(piece):
        return piece in (WHITE_KING,BLACK_KING,)
    @staticmethod
    def is_piece_of_player(piece, player):
        if player == PLAYER_WHITE:
            return ChessRules.is_white_piece(piece)
        if player == PLAYER_BLACK:
            return ChessRules.is_black_piece(piece)
        return False
    @staticmethod
    def is_valid_position(row, column):
        return (0 <= row < BOARD_ROWS and 0 <= column < BOARD_COLUMNS)
    @staticmethod
    def is_same_position(position_a, position_b):
        return position_a == position_b
    @staticmethod
    def get_pawn_direction(player):
        if player == PLAYER_WHITE:
            return WHITE_PAWN_DIRECTION
        if player == PLAYER_BLACK:
            return BLACK_PAWN_DIRECTION
        return 0
    @staticmethod
    def get_pawn_start_row(player):
        if player == PLAYER_WHITE:
            return 6
        if player == PLAYER_BLACK:
            return 1
        return None
    @staticmethod
    def get_promotion_row(player):
        if player == PLAYER_WHITE:
            return WHITE_PROMOTION_ROW
        if player == PLAYER_BLACK:
            return BLACK_PROMOTION_ROW
        return None
    @staticmethod
    def is_valid_promotion_type(promotion_type):
        return promotion_type in (PROMOTION_NONE,PROMOTION_QUEEN,PROMOTION_ROOK,PROMOTION_BISHOP,PROMOTION_KNIGHT,)
    @staticmethod
    def get_promotion_piece(player, promotion_type):
        if promotion_type == PROMOTION_NONE:
            return (WHITE_PAWN if player == PLAYER_WHITE else BLACK_PAWN)
        if player == PLAYER_WHITE:
            pieces = {PROMOTION_QUEEN: WHITE_QUEEN,PROMOTION_ROOK: WHITE_ROOK,PROMOTION_BISHOP: WHITE_BISHOP,PROMOTION_KNIGHT: WHITE_KNIGHT,}
        elif player == PLAYER_BLACK:
            pieces = {PROMOTION_QUEEN: BLACK_QUEEN,PROMOTION_ROOK: BLACK_ROOK,PROMOTION_BISHOP: BLACK_BISHOP,PROMOTION_KNIGHT: BLACK_KNIGHT,}
        else:
            return EMPTY
        return pieces.get(promotion_type,EMPTY,)
    @staticmethod
    def is_promotion_move(board, move, player):
        if not ChessRules.is_valid_move_format(move):
            return False
        from_row, _, to_row, _ = move[:4]
        piece = board.get_cell(from_row,move[1],)
        if not ChessRules.is_pawn(piece):
            return False
        return (to_row == ChessRules.get_promotion_row(player))
    @staticmethod
    def is_valid_move_format(move):
        if not isinstance(move, tuple):
            return False
        if len(move) not in (4, 5):
            return False
        return all(isinstance(value, int) for value in move[:4])
    @staticmethod
    def get_pawn_moves(board, row, column, player):
        moves = []
        direction = ChessRules.get_pawn_direction(player)
        start_row = ChessRules.get_pawn_start_row(player)
        next_row = row + direction
        if ChessRules.is_valid_position(next_row,column,):
            if board.is_empty(next_row,column,):
                moves.append((row,column,next_row,column,))
                double_row = (row + 2 * direction)
                if (row == start_row and board.is_empty(double_row,column,)):
                    moves.append((row,column,double_row,column,))
        for delta_column in (-1, 1):
            target_row = row + direction
            target_column = (column + delta_column)
            if not ChessRules.is_valid_position(target_row,target_column,):
                continue
            target = board.get_cell(target_row,target_column,)
            if (target != EMPTY and ChessRules.is_piece_of_player(target,ChessRules.get_opponent(player),) and not ChessRules.is_king(target)):
                moves.append((row,column,target_row,target_column,))
        return moves
    @staticmethod
    def get_knight_moves(board,row,column,player,):
        moves = []
        for delta_row, delta_column in KNIGHT_DIRECTIONS:
            target_row = row + delta_row
            target_column = (column + delta_column)
            if not ChessRules.is_valid_position(target_row,target_column,):
                continue
            target = board.get_cell(target_row,target_column,)
            if (target == EMPTY or (ChessRules.is_piece_of_player(target,ChessRules.get_opponent(player),) and not ChessRules.is_king(target))):
                moves.append((row,column,target_row,target_column,))
        return moves
    @staticmethod
    def get_sliding_moves(board,row,column,player,directions,):
        moves = []
        opponent = ChessRules.get_opponent(player)
        for delta_row, delta_column in directions:
            target_row = row + delta_row
            target_column = (column + delta_column)
            while ChessRules.is_valid_position(target_row,target_column,):
                target = board.get_cell(target_row,target_column,)
                if target == EMPTY:
                    moves.append((row,column,target_row,target_column,))
                else:
                    if (ChessRules.is_piece_of_player(target,opponent,) and not ChessRules.is_king(target)):
                        moves.append((row,column,target_row,target_column,))
                    break
                target_row += delta_row
                target_column += delta_column
        return moves
    @staticmethod
    def get_bishop_moves(board,row,column,player,):
        return ChessRules.get_sliding_moves(board,row,column,player,BISHOP_DIRECTIONS,)
    @staticmethod
    def get_rook_moves(board,row,column,player,):
        return ChessRules.get_sliding_moves(board,row,column,player,ROOK_DIRECTIONS,)
    @staticmethod
    def get_queen_moves(board,row,column,player,):
        return ChessRules.get_sliding_moves(board,row,column,player,QUEEN_DIRECTIONS,)
    @staticmethod
    def get_king_moves(board,row,column,player,):
        moves = []
        opponent = ChessRules.get_opponent(player)
        for delta_row, delta_column in KING_DIRECTIONS:
            target_row = row + delta_row
            target_column = (column + delta_column)
            if not ChessRules.is_valid_position(target_row,target_column,):
                continue
            target = board.get_cell(target_row,target_column,)
            if target == EMPTY:
                moves.append((row,column,target_row,target_column,))
            elif (ChessRules.is_piece_of_player(target,opponent,) and not ChessRules.is_king(target)):
                moves.append((row,column,target_row,target_column,))
        return moves
    @staticmethod
    def get_piece_moves(board,row,column,player,):
        piece = board.get_cell(row,column,)
        if not ChessRules.is_piece_of_player(piece,player,):
            return []
        if ChessRules.is_pawn(piece):
            return ChessRules.get_pawn_moves(board,row,column,player,)
        if ChessRules.is_knight(piece):
            return ChessRules.get_knight_moves(board,row,column,player,)
        if ChessRules.is_bishop(piece):
            return ChessRules.get_bishop_moves(board,row,column,player,)
        if ChessRules.is_rook(piece):
            return ChessRules.get_rook_moves(board,row,column,player,)
        if ChessRules.is_queen(piece):
            return ChessRules.get_queen_moves(board,row,column,player,)
        if ChessRules.is_king(piece):
            return ChessRules.get_king_moves(board,row,column,player,)
        return []
    @staticmethod
    def is_square_attacked(board,row,column,by_player,):
        if not ChessRules.is_valid_player(by_player):
            return False
        opponent = ChessRules.get_opponent(by_player)
        pawn_direction = (ChessRules.get_pawn_direction(by_player))
        pawn_row = row - pawn_direction
        for pawn_column in (column - 1,column + 1,):
            if not ChessRules.is_valid_position(pawn_row,pawn_column,):
                continue
            piece = board.get_cell(pawn_row,pawn_column,)
            if (piece == (WHITE_PAWN if by_player == PLAYER_WHITE else BLACK_PAWN)):
                return True
        knight = (WHITE_KNIGHT if by_player == PLAYER_WHITE else BLACK_KNIGHT)
        for delta_row, delta_column in KNIGHT_DIRECTIONS:
            source_row = row + delta_row
            source_column = (column + delta_column)
            if not ChessRules.is_valid_position(source_row,source_column,):
                continue
            if board.get_cell(source_row,source_column,) == knight:
                return True
        king = (WHITE_KING if by_player == PLAYER_WHITE else BLACK_KING)
        for delta_row, delta_column in KING_DIRECTIONS:
            source_row = row + delta_row
            source_column = (column + delta_column)
            if not ChessRules.is_valid_position(source_row,source_column,):
                continue
            if board.get_cell(source_row,source_column,) == king:
                return True
        bishop = (WHITE_BISHOP if by_player == PLAYER_WHITE else BLACK_BISHOP)
        rook = (WHITE_ROOK if by_player == PLAYER_WHITE else BLACK_ROOK)
        queen = (WHITE_QUEEN if by_player == PLAYER_WHITE else BLACK_QUEEN)
        for delta_row, delta_column in BISHOP_DIRECTIONS:
            source_row = row + delta_row
            source_column = (column + delta_column)
            while ChessRules.is_valid_position(source_row,source_column,):
                piece = board.get_cell(source_row,source_column,)
                if piece != EMPTY:
                    if piece in (bishop,queen,):
                        return True
                    break
                source_row += delta_row
                source_column += delta_column
        for delta_row, delta_column in ROOK_DIRECTIONS:
            source_row = row + delta_row
            source_column = (column + delta_column)
            while ChessRules.is_valid_position(source_row,source_column,):
                piece = board.get_cell(source_row,source_column,)
                if piece != EMPTY:
                    if piece in (rook,queen,):
                        return True
                    break
                source_row += delta_row
                source_column += delta_column
        return False
    @staticmethod
    def is_in_check(board,player,):
        king_position = board.find_king(player)
        if king_position is None:
            return True
        king_row, king_column = king_position
        return ChessRules.is_square_attacked(board,king_row,king_column,ChessRules.get_opponent(player),)
    @staticmethod
    def is_en_passant_move(board,move,player,en_passant_target=None,):
        if en_passant_target is None:
            return False
        if not ChessRules.is_valid_move_format(move):
            return False
        if len(move) == 5:
            move = move[:4]
        from_row, from_column, to_row, to_column = move
        if move[2:] != en_passant_target:
            return False
        piece = board.get_cell(from_row,from_column,)
        if not ChessRules.is_pawn(piece):
            return False
        if not ChessRules.is_piece_of_player(piece,player,):
            return False
        if not board.is_empty(to_row,to_column,):
            return False
        direction = ChessRules.get_pawn_direction(player)
        if to_row - from_row != direction:
            return False
        if abs(to_column - from_column) != 1:
            return False
        capture_row = to_row - direction
        captured_piece = board.get_cell(capture_row,to_column,)
        opponent_pawn = (BLACK_PAWN if player == PLAYER_WHITE else WHITE_PAWN)
        return captured_piece == opponent_pawn
    @staticmethod
    def get_en_passant_capture_position(move,player,):
        if not ChessRules.is_valid_move_format(move):
            return None
        from_row, _, to_row, to_column = move[:4]
        direction = ChessRules.get_pawn_direction(player)
        return (to_row - direction,to_column,)
    @staticmethod
    def _get_castling_data(player,castling_type,):
        if player == PLAYER_WHITE:
            row = 7
            if castling_type == CASTLING_KINGSIDE:
                return ((7, 4),(7, 7),(7, 6),(7, 5),("white_kingside"),)
            if castling_type == CASTLING_QUEENSIDE:
                return ((7, 4),(7, 0),(7, 2),(7, 3),("white_queenside"),)
        elif player == PLAYER_BLACK:
            row = 0
            if castling_type == CASTLING_KINGSIDE:
                return ((0, 4),(0, 7),(0, 6),(0, 5),("black_kingside"),)
            if castling_type == CASTLING_QUEENSIDE:
                return ((0, 4),(0, 0),(0, 2),(0, 3),("black_queenside"),)
        return None
    @staticmethod
    def get_castling_type(move, player):
        if not ChessRules.is_valid_move_format(move):
            return None
        from_row, from_column, to_row, to_column = (move[:4])
        if player == PLAYER_WHITE:
            expected_row = 7
        elif player == PLAYER_BLACK:
            expected_row = 0
        else:
            return None
        if (from_row != expected_row or from_column != 4 or to_row != expected_row):
            return None
        if to_column == 6:
            return CASTLING_KINGSIDE
        if to_column == 2:
            return CASTLING_QUEENSIDE
        return None
    @staticmethod
    def is_castling_move(board,move,player,castling_rights=None,):
        castling_type = ChessRules.get_castling_type(move,player,)
        if castling_type is None:
            return False
        if castling_rights is None:
            return False
        data = ChessRules._get_castling_data(player,castling_type,)
        if data is None:
            return False
        (king_position,rook_position,destination,rook_destination,rights_key,) = data
        if not castling_rights.get(rights_key,False,):
            return False
        king_row, king_column = king_position
        rook_row, rook_column = rook_position
        king = (WHITE_KING if player == PLAYER_WHITE else BLACK_KING)
        rook = (WHITE_ROOK if player == PLAYER_WHITE else BLACK_ROOK)
        if board.get_cell(king_row,king_column,) != king:
            return False
        if board.get_cell(rook_row,rook_column,) != rook:
            return False
        if castling_type == CASTLING_KINGSIDE:
            empty_columns = (5, 6)
        else:
            empty_columns = (1, 2, 3)
        for column in empty_columns:
            if not board.is_empty(king_row,column,):
                return False
        opponent = ChessRules.get_opponent(player)
        if ChessRules.is_square_attacked(board,king_row,king_column,opponent,):
            return False
        transit_column = (5 if castling_type == CASTLING_KINGSIDE else 3)
        if ChessRules.is_square_attacked(board,king_row,transit_column,opponent,):
            return False
        destination_column = (6 if castling_type == CASTLING_KINGSIDE else 2)
        if ChessRules.is_square_attacked(board,king_row,destination_column,opponent,):
            return False
        return True
    @staticmethod
    def get_castling_rook_move(move,player,):
        castling_type = ChessRules.get_castling_type(move,player,)
        if castling_type == CASTLING_KINGSIDE:
            if player == PLAYER_WHITE:
                return ((7, 7),(7, 5),)
            if player == PLAYER_BLACK:
                return ((0, 7),(0, 5),)
        elif castling_type == CASTLING_QUEENSIDE:
            if player == PLAYER_WHITE:
                return ((7, 0),(7, 3),)
            if player == PLAYER_BLACK:
                return ((0, 0),(0, 3),)
        return None
    @staticmethod
    def is_valid_move(board,move,player,en_passant_target=None,castling_rights=None,):
        if not ChessRules.is_valid_move_format(move):
            return False
        if not ChessRules.is_valid_player(player):
            return False
        from_row, from_column, to_row, to_column = (move[:4])
        if not ChessRules.is_valid_position(from_row,from_column,):
            return False
        if not ChessRules.is_valid_position(to_row,to_column,):
            return False
        if (from_row == to_row and from_column == to_column):
            return False
        piece = board.get_cell(from_row,from_column,)
        if not ChessRules.is_piece_of_player(piece,player,):
            return False
        target = board.get_cell(to_row,to_column,)
        if ChessRules.is_piece_of_player(target,player,):
            return False
        if ChessRules.get_castling_type(move,player,) is not None:
            return ChessRules.is_castling_move(board,move,player,castling_rights,)
        if ChessRules.is_en_passant_move(board,move,player,en_passant_target,):
            return True
        return move[:4] in ChessRules.get_piece_moves(board,from_row,from_column,player,)
    @staticmethod
    def is_legal_move(board,move,player,en_passant_target=None,castling_rights=None,):
        if not ChessRules.is_valid_move(board,move,player,en_passant_target,castling_rights,):
            return False
        simulated_board = board.copy()
        if not ChessRules.apply_move(simulated_board,move,player,en_passant_target,castling_rights,):
            return False
        return not ChessRules.is_in_check(simulated_board,player,)
    @staticmethod
    def get_legal_moves(board,player,en_passant_target=None,castling_rights=None,):
        legal_moves = []
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                piece = board.get_cell(row,column,)
                if not ChessRules.is_piece_of_player(piece,player):
                    continue
                candidate_moves = (ChessRules.get_piece_moves(board,row,column,player,))
                for move in candidate_moves:
                    if ChessRules.is_legal_move(board,move,player,en_passant_target,castling_rights,):
                        legal_moves.append(move)
        if en_passant_target is not None:
            target_row, target_column = (en_passant_target)
            direction = (ChessRules.get_pawn_direction(player))
            source_row = (target_row - direction)
            for source_column in (target_column - 1,target_column + 1,):
                if not ChessRules.is_valid_position(source_row,source_column,):
                    continue
                piece = board.get_cell(source_row,source_column,)
                if not ChessRules.is_pawn(piece):
                    continue
                if not ChessRules.is_piece_of_player(piece,player,):
                    continue
                move = (source_row,source_column,target_row,target_column,)
                if ChessRules.is_legal_move(board,move,player,en_passant_target,castling_rights,):
                    legal_moves.append(move)
        king_position = board.find_king(player)
        if king_position is not None:
            king_row, king_column = (king_position)
            if king_column == 4:
                for destination_column in (6,2,):
                    move = (king_row,king_column,king_row,destination_column,)
                    if ChessRules.is_legal_move(board,move,player,en_passant_target,castling_rights,):
                        legal_moves.append(move)
        return legal_moves
    @staticmethod
    def get_all_piece_moves(board,player,en_passant_target=None,castling_rights=None,):
        return ChessRules.get_legal_moves(board,player,en_passant_target,castling_rights,)
    @staticmethod
    def apply_move(board,move,player,en_passant_target=None,castling_rights=None,):
        if not ChessRules.is_valid_move_format(move):
            return False
        if len(move) == 5:
            promotion_type = move[4]
        else:
            promotion_type = PROMOTION_NONE
        from_row, from_column, to_row, to_column = (move[:4])
        if not ChessRules.is_valid_position(from_row,from_column,):
            return False
        if not ChessRules.is_valid_position(to_row,to_column,):
            return False
        piece = board.get_cell(from_row,from_column,)
        if not ChessRules.is_piece_of_player(piece,player,):
            return False
        target = board.get_cell(to_row,to_column,)
        if ChessRules.get_castling_type(move,player,) is not None:
            if not ChessRules.is_castling_move(board,move,player,castling_rights,):
                return False
            rook_move = (ChessRules.get_castling_rook_move(move,player,))
            if rook_move is None:
                return False
            (rook_from,rook_to,) = rook_move
            rook_piece = board.get_cell(rook_from[0],rook_from[1],)
            board.set_cell(to_row,to_column,piece,)
            board.set_cell(from_row,from_column,EMPTY,)
            board.set_cell(rook_to[0],rook_to[1],rook_piece,)
            board.set_cell(rook_from[0],rook_from[1],EMPTY,)
            return True
        is_en_passant = (ChessRules.is_en_passant_move(board,move,player,en_passant_target,))
        if is_en_passant:
            capture_position = (ChessRules.get_en_passant_capture_position(move,player,))
            if capture_position is None:
                return False
            capture_row, capture_column = (capture_position)
            board.set_cell(capture_row,capture_column,EMPTY,)
        if ChessRules.is_promotion_move(board,move,player,):
            if not ChessRules.is_valid_promotion_type(promotion_type):
                return False
            if promotion_type == PROMOTION_NONE:
                promotion_type = PROMOTION_QUEEN
            promoted_piece = (
                ChessRules.get_promotion_piece(player,promotion_type,))
            if promoted_piece == EMPTY:
                return False
            board.set_cell(from_row,from_column,EMPTY,)
            board.set_cell(to_row,to_column,promoted_piece,)
            return True
        board.set_cell(from_row,from_column,EMPTY,)
        board.set_cell(to_row,to_column,piece,)
        return True
    @staticmethod
    def apply_legal_move(board,move,player,en_passant_target=None,castling_rights=None,):
        if not ChessRules.is_legal_move(board,move,player,en_passant_target,castling_rights,):
            return False
        return ChessRules.apply_move(board,move,player,en_passant_target,castling_rights,)
    @staticmethod
    def is_capture_move(board,move,player,en_passant_target=None,castling_rights=None,):
        if not ChessRules.is_valid_move_format(move):
            return False
        if ChessRules.is_en_passant_move(board,move,player,en_passant_target,):
            return True
        _, _, to_row, to_column = move[:4]
        target = board.get_cell(to_row,to_column,)
        return (target != EMPTY and ChessRules.is_piece_of_player(target,ChessRules.get_opponent(player),) and not ChessRules.is_king(target))
    @staticmethod
    def evaluate_game(board,player,en_passant_target=None,castling_rights=None,):
        result = GameResult()
        if board.find_king(PLAYER_WHITE) is None:
            result.winner = PLAYER_BLACK
            result.game_over = True
            return result
        if board.find_king(PLAYER_BLACK) is None:
            result.winner = PLAYER_WHITE
            result.game_over = True
            return result
        legal_moves = ChessRules.get_legal_moves(board,player,en_passant_target,castling_rights,)
        if legal_moves:
            return result
        if ChessRules.is_in_check(board,player,):
            result.winner = (ChessRules.get_opponent(player))
            result.game_over = True
            return result
        result.draw = True
        result.game_over = True
        return result
    @staticmethod
    def get_piece_value(piece):
        from games.chess.constants import (PAWN_VALUE,KNIGHT_VALUE,BISHOP_VALUE,ROOK_VALUE,QUEEN_VALUE,KING_VALUE,EMPTY,)
        values = {EMPTY: 0,WHITE_PAWN: PAWN_VALUE,WHITE_KNIGHT: KNIGHT_VALUE,WHITE_BISHOP: BISHOP_VALUE,WHITE_ROOK: ROOK_VALUE,WHITE_QUEEN: QUEEN_VALUE,WHITE_KING: KING_VALUE,BLACK_PAWN: PAWN_VALUE,BLACK_KNIGHT: KNIGHT_VALUE,BLACK_BISHOP: BISHOP_VALUE,BLACK_ROOK: ROOK_VALUE,BLACK_QUEEN: QUEEN_VALUE,BLACK_KING: KING_VALUE,}
        return values.get(piece,0,)
    @staticmethod
    def evaluate_material(board):
        white_score = 0
        black_score = 0
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                piece = board.get_cell(row,column,)
                value = ChessRules.get_piece_value(piece)
                if ChessRules.is_white_piece(piece):
                    white_score += value
                elif ChessRules.is_black_piece(piece):
                    black_score += value
        return white_score - black_score
    @staticmethod
    def get_material_score(board, player):
        evaluation = ChessRules.evaluate_material(board)
        if player == PLAYER_WHITE:
            return evaluation
        if player == PLAYER_BLACK:
            return -evaluation
        raise ValueError(f"Invalid player: {player}")