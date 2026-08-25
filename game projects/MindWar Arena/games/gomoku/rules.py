# games/gomoku/rules.py
from engine.interfaces.game_result import GameResult
from games.gomoku.constants import (BOARD_ROWS,BOARD_COLUMNS,WIN_LENGTH,EMPTY,NO_WINNER,)
class GomokuRules:
    _DIRECTIONS = ((0, 1),(1, 0),(1, 1),(1, -1),)
    @staticmethod
    def check_winner(board):
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                player = board.get_cell(row, column)
                if player == EMPTY:
                    continue
                for row_delta, column_delta in GomokuRules._DIRECTIONS:
                    if GomokuRules._check_direction(board, row, column, row_delta, column_delta, player,):
                        return player
        return NO_WINNER
    @staticmethod
    def get_winning_cells(board):
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                player = board.get_cell(row, column)
                if player == EMPTY:
                    continue
                for row_delta, column_delta in GomokuRules._DIRECTIONS:
                    cells = GomokuRules._collect_direction(board, row, column, row_delta, column_delta, player, )
                    if cells:
                        return cells
        return []
    @staticmethod
    def is_draw(board):
        return (GomokuRules.check_winner(board) == NO_WINNER and board.is_board_full())
    @staticmethod
    def is_game_over(board):
        if GomokuRules.check_winner(board) != NO_WINNER:
            return True
        if board.is_board_full():
            return True
        return False
    @staticmethod
    def evaluate_game(board):
        result = GameResult()
        winner = GomokuRules.check_winner(board)
        if winner != NO_WINNER:
            result.winner = winner
            result.game_over = True
            result.winning_cells = GomokuRules.get_winning_cells(board)
            return result
        if board.is_board_full():
            result.draw = True
            result.game_over = True
            return result
        return result
    @staticmethod
    def _check_direction(board, row, column, row_delta, column_delta, player, ):
        for index in range(1, WIN_LENGTH):
            next_row = row + row_delta * index
            next_column = column + column_delta * index
            if not board.is_valid_position(next_row,next_column,):
                return False
            if board.get_cell(next_row, next_column,) != player:
                return False
        return True
    @staticmethod
    def _collect_direction(board,row,column,row_delta,column_delta,player,):
        cells = []
        for index in range(WIN_LENGTH):
            next_row = row + row_delta * index
            next_column = column + column_delta * index
            if not board.is_valid_position(next_row, next_column,):
                return []
            if board.get_cell(next_row,next_column,) != player:
                return []
            cells.append((next_row, next_column))
        return cells