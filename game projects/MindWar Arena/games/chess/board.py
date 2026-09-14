# games/chess/board.py
from copy import deepcopy
from games.chess.constants import (BLACK_BISHOP,BLACK_KING,BLACK_KNIGHT,BLACK_PAWN,BLACK_QUEEN,BLACK_ROOK,BOARD_COLUMNS,BOARD_ROWS,DARK_SQUARE,EMPTY,LIGHT_SQUARE,PLAYER_BLACK,PLAYER_WHITE,WHITE_BISHOP,WHITE_KING,WHITE_KNIGHT,WHITE_PAWN,WHITE_QUEEN,WHITE_ROOK,)
class ChessBoard:
    def __init__(self):
        self._board = []
        self.reset()
    def reset(self):
        self._board = [[EMPTY for _ in range(BOARD_COLUMNS)]for _ in range(BOARD_ROWS)]
        self._board[0] = [BLACK_ROOK,BLACK_KNIGHT,BLACK_BISHOP,BLACK_QUEEN,BLACK_KING,BLACK_BISHOP,BLACK_KNIGHT,BLACK_ROOK,]
        self._board[1] = [BLACK_PAWN for _ in range(BOARD_COLUMNS)]
        self._board[6] = [WHITE_PAWN for _ in range(BOARD_COLUMNS)]
        self._board[7] = [WHITE_ROOK,WHITE_KNIGHT,WHITE_BISHOP,WHITE_QUEEN,WHITE_KING,WHITE_BISHOP,WHITE_KNIGHT,WHITE_ROOK,]
    def get_cell(self, row, column):
        if not self.is_valid_position(row, column):
            raise ValueError(f"Invalid board position: ({row}, {column})")
        return self._board[row][column]
    def set_cell(self, row, column, value):
        if not self.is_valid_position(row, column):
            raise ValueError(f"Invalid board position: ({row}, {column})")
        if not self.is_valid_piece(value):
            raise ValueError(f"Invalid piece value: {value}")
        self._board[row][column] = value
    def is_valid_position(self, row, column):
        return (0 <= row < BOARD_ROWS and 0 <= column < BOARD_COLUMNS)
    def get_square_color(self, row, column):
        if not self.is_valid_position(row, column):
            raise ValueError(f"Invalid board position: ({row}, {column})")
        if (row + column) % 2 == 0:
            return LIGHT_SQUARE
        return DARK_SQUARE
    def is_light_square(self, row, column):
        return (self.get_square_color(row, column) == LIGHT_SQUARE)
    def is_dark_square(self, row, column):
        return (self.get_square_color(row, column) == DARK_SQUARE)
    def is_empty(self, row, column):
        return (self.get_cell(row, column) == EMPTY)
    def is_valid_piece(self, piece):
        return piece in (EMPTY,WHITE_PAWN,WHITE_KNIGHT,WHITE_BISHOP,WHITE_ROOK,WHITE_QUEEN,WHITE_KING,BLACK_PAWN,BLACK_KNIGHT,BLACK_BISHOP,BLACK_ROOK,BLACK_QUEEN,BLACK_KING,)
    @staticmethod
    def is_white_piece(piece):
        return piece in (WHITE_PAWN,WHITE_KNIGHT,WHITE_BISHOP,WHITE_ROOK,WHITE_QUEEN,WHITE_KING,)
    @staticmethod
    def is_black_piece(piece):
        return piece in (BLACK_PAWN,BLACK_KNIGHT,BLACK_BISHOP,BLACK_ROOK,BLACK_QUEEN,BLACK_KING,)
    @staticmethod
    def is_player_piece(piece, player):
        if player == PLAYER_WHITE:
            return ChessBoard.is_white_piece(piece)
        if player == PLAYER_BLACK:
            return ChessBoard.is_black_piece(piece)
        return False
    @staticmethod
    def get_piece_player(piece):
        if ChessBoard.is_white_piece(piece):
            return PLAYER_WHITE
        if ChessBoard.is_black_piece(piece):
            return PLAYER_BLACK
        return None
    def get_piece_positions(self, player):
        positions = []
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                piece = self._board[row][column]
                if self.is_player_piece(piece,player,):
                    positions.append((row, column))
        return positions
    def get_all_piece_positions(self):
        positions = []
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                if self._board[row][column] != EMPTY:
                    positions.append((row, column))
        return positions
    def count_pieces(self, player):
        return len(self.get_piece_positions(player))
    def count_piece(self, piece):
        count = 0
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                if self._board[row][column] == piece:
                    count += 1
        return count
    def find_piece(self, piece):
        positions = []
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                if self._board[row][column] == piece:
                    positions.append((row, column))
        return positions
    def find_king(self, player):
        if player == PLAYER_WHITE:
            king = WHITE_KING
        elif player == PLAYER_BLACK:
            king = BLACK_KING
        else:
            return None
        positions = self.find_piece(king)
        if not positions:
            return None
        return positions[0]
    def get_board_state(self):
        return deepcopy(self._board)
    def copy(self):
        new_board = ChessBoard()
        new_board._board = deepcopy(self._board)
        return new_board
    def __str__(self):
        symbols = {EMPTY: ".",WHITE_PAWN: "P",WHITE_KNIGHT: "N",WHITE_BISHOP: "B",WHITE_ROOK: "R",WHITE_QUEEN: "Q",WHITE_KING: "K",BLACK_PAWN: "p",BLACK_KNIGHT: "n",BLACK_BISHOP: "b",BLACK_ROOK: "r",BLACK_QUEEN: "q",BLACK_KING: "k",}
        rows = []
        for row in self._board:
            rows.append(" ".join(symbols[piece] for piece in row))
        return "\n".join(rows)