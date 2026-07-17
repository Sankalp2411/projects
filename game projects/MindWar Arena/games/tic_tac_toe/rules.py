from engine.interfaces.game_result import GameResult
from games.tic_tac_toe.constants import (BOARD_ROWS,BOARD_COLUMNS,EMPTY,NO_WINNER,)
class TicTacToeRules:
    @staticmethod
    def check_winner(board):
        for row in range(BOARD_ROWS):
            first = board.get_cell(row, 0)
            if first == EMPTY:
                continue
            winner = True
            for column in range(1, BOARD_COLUMNS):
                if board.get_cell(row, column) != first:
                    winner = False
                    break
            if winner:
                return first
        for column in range(BOARD_COLUMNS):
            first = board.get_cell(0, column)
            if first == EMPTY:
                continue
            winner = True
            for row in range(1, BOARD_ROWS):
                if board.get_cell(row, column) != first:
                    winner = False
                    break
            if winner:
                return first
        first = board.get_cell(0, 0)
        if first != EMPTY:
            winner = True
            for index in range(1, BOARD_ROWS):
                if board.get_cell(index, index) != first:
                    winner = False
                    break
            if winner:
                return first
        first = board.get_cell(0, BOARD_COLUMNS - 1)
        if first != EMPTY:
            winner = True
            for index in range(1, BOARD_ROWS):
                if board.get_cell(index, BOARD_COLUMNS - 1 - index) != first:
                    winner = False
                    break
            if winner:
                return first
        return NO_WINNER
    @staticmethod
    def get_winning_cells(board):
        for row in range(BOARD_ROWS):
            first = board.get_cell(row, 0)
            if first == EMPTY:
                continue
            winner = True
            for column in range(1, BOARD_COLUMNS):
                if board.get_cell(row, column) != first:
                    winner = False
                    break
            if winner:
                return [(row, column) for column in range(BOARD_COLUMNS)]
        for column in range(BOARD_COLUMNS):
            first = board.get_cell(0, column)
            if first == EMPTY:
                continue
            winner = True
            for row in range(1, BOARD_ROWS):
                if board.get_cell(row, column) != first:
                    winner = False
                    break
            if winner:
                return [(row, column) for row in range(BOARD_ROWS)]
        first = board.get_cell(0, 0)
        if first != EMPTY:
            winner = True
            for index in range(1, BOARD_ROWS):
                if board.get_cell(index, index) != first:
                    winner = False
                    break
            if winner:
                return [(index, index) for index in range(BOARD_ROWS)]
        first = board.get_cell(0, BOARD_COLUMNS - 1)
        if first != EMPTY:
            winner = True
            for index in range(1, BOARD_ROWS):
                if (board.get_cell(index,BOARD_COLUMNS - 1 - index,)!= first):
                    winner = False
                    break
            if winner:
                return [(index,BOARD_COLUMNS - 1 - index,) for index in range(BOARD_ROWS)]
        return []
    @staticmethod
    def is_draw(board):
        return (TicTacToeRules.check_winner(board) == NO_WINNER and board.is_board_full())
    @staticmethod
    def is_game_over(board):
        if TicTacToeRules.check_winner(board) != NO_WINNER:
            return True
        if board.is_board_full():
            return True
        return False
    @staticmethod
    def evaluate_game(board):
        result = GameResult()
        winner = TicTacToeRules.check_winner(board)
        if winner != NO_WINNER:
            result.winner = winner
            result.game_over = True
            result.winning_cells = TicTacToeRules.get_winning_cells(board)
            return result
        if board.is_board_full():
            result.draw = True
            result.game_over = True
            return result
        return result