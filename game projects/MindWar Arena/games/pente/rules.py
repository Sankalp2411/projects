# games/pente/rules.py
from engine.interfaces.game_result import GameResult
from games.pente.constants import (BOARD_ROWS,BOARD_COLUMNS,WIN_LENGTH,EMPTY,PLAYER_BLACK,PLAYER_WHITE,NO_WINNER,CAPTURE_WIN_PAIRS,)
class PenteRules:
    _DIRECTIONS = ((0, 1),(1, 0),(1, 1),(1, -1),)
    @staticmethod
    def get_opponent(player):
        if player == PLAYER_BLACK:
            return PLAYER_WHITE
        if player == PLAYER_WHITE:
            return PLAYER_BLACK
        return EMPTY
    @staticmethod
    def check_winner(board):
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                player = board.get_cell(row, column)
                if player == EMPTY:
                    continue
                for row_delta, column_delta in PenteRules._DIRECTIONS:
                    if PenteRules._check_direction(board,row,column,row_delta,column_delta,player,):
                        return player
        return NO_WINNER
    @staticmethod
    def get_winning_cells(board):
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                player = board.get_cell(row, column)
                if player == EMPTY:
                    continue
                for row_delta, column_delta in PenteRules._DIRECTIONS:
                    cells = PenteRules._collect_direction(board,row,column,row_delta,column_delta,player,)
                    if cells:
                        return cells
        return []
    @staticmethod
    def get_captures(board, row, column, player):
        if not board.is_valid_position(row, column):
            return []
        if board.get_cell(row, column) != player:
            return []
        opponent = PenteRules.get_opponent(player)
        if opponent == EMPTY:
            return []
        captures = []
        for row_delta, column_delta in PenteRules._DIRECTIONS:
            capture = PenteRules._check_capture_pattern(board,row,column,row_delta,column_delta,player,opponent,)
            if capture:
                captures.append(capture)
            capture = PenteRules._check_capture_pattern(board,row,column,-row_delta,-column_delta,player,opponent,)
            if capture:
                captures.append(capture)
        return PenteRules._remove_duplicate_captures(captures)
    @staticmethod
    def find_captures(board, row, column, player):
        captures = PenteRules.get_captures(board,row,column,player,)
        captured_cells = []
        for capture in captures:
            for cell in capture:
                if cell not in captured_cells:
                    captured_cells.append(cell)
        return captured_cells
    @staticmethod
    def _check_capture_pattern(board,row,column,row_delta,column_delta,player,opponent,):
        first_row = row + row_delta
        first_column = column + column_delta
        second_row = row + row_delta * 2
        second_column = column + column_delta * 2
        third_row = row + row_delta * 3
        third_column = column + column_delta * 3
        if not board.is_valid_position(first_row,first_column,):
            return None
        if not board.is_valid_position(second_row,second_column,):
            return None
        if not board.is_valid_position(third_row,third_column,):
            return None
        if board.get_cell(first_row,first_column,) != opponent:
            return None
        if board.get_cell(second_row,second_column,) != opponent:
            return None
        if board.get_cell(third_row,third_column,) != player:
            return None
        return ((first_row, first_column),(second_row, second_column),)
    @staticmethod
    def _remove_duplicate_captures(captures):
        unique_captures = []
        for capture in captures:
            if capture not in unique_captures:
                unique_captures.append(capture)
        return unique_captures
    @staticmethod
    def apply_captures(board, captures):
        if not captures:
            return 0
        captured_cells = []
        first_item = captures[0]
        if (isinstance(first_item, tuple) and len(first_item) == 2 and isinstance(first_item[0], tuple)):
            for capture in captures:
                for cell in capture:
                    if cell not in captured_cells:
                        captured_cells.append(cell)
        else:
            for cell in captures:
                if cell not in captured_cells:
                    captured_cells.append(cell)
        captured_count = 0
        for row, column in captured_cells:
            if not board.is_valid_position(row, column):
                continue
            if board.get_cell(row, column) == EMPTY:
                continue
            if board.remove_stone(row, column):
                captured_count += 1
        return captured_count
    @staticmethod
    def is_draw(board, capture_counts=None):
        if PenteRules.check_winner(board) != NO_WINNER:
            return False
        if capture_counts is not None:
            black_captures = capture_counts.get(PLAYER_BLACK,0,)
            white_captures = capture_counts.get(PLAYER_WHITE,0,)
            if black_captures >= CAPTURE_WIN_PAIRS:
                return False
            if white_captures >= CAPTURE_WIN_PAIRS:
                return False
        return board.is_board_full()
    @staticmethod
    def is_game_over(board,capture_counts=None,black_captures=0,white_captures=0,):
        if PenteRules.check_winner(board) != NO_WINNER:
            return True
        if capture_counts is not None:
            black_captures = capture_counts.get(PLAYER_BLACK,0,)
            white_captures = capture_counts.get(PLAYER_WHITE,0,)
        if black_captures >= CAPTURE_WIN_PAIRS:
            return True
        if white_captures >= CAPTURE_WIN_PAIRS:
            return True
        if board.is_board_full():
            return True
        return False
    @staticmethod
    def evaluate_game(board,capture_counts=None,black_captures=0,white_captures=0,):
        result = GameResult()
        winner = PenteRules.check_winner(board)
        if winner != NO_WINNER:
            result.winner = winner
            result.game_over = True
            result.winning_cells = (PenteRules.get_winning_cells(board))
            return result
        if capture_counts is not None:
            black_captures = capture_counts.get(PLAYER_BLACK,0,)
            white_captures = capture_counts.get(PLAYER_WHITE,0,)
        if black_captures >= CAPTURE_WIN_PAIRS:
            result.winner = PLAYER_BLACK
            result.game_over = True
            return result
        if white_captures >= CAPTURE_WIN_PAIRS:
            result.winner = PLAYER_WHITE
            result.game_over = True
            return result
        if board.is_board_full():
            result.draw = True
            result.game_over = True
            return result
        return result
    @staticmethod
    def _check_direction(board,row,column,row_delta,column_delta,player,):
        for index in range(1, WIN_LENGTH):
            next_row = row + row_delta * index
            next_column = column + column_delta * index
            if not board.is_valid_position(next_row,next_column,):
                return False
            if board.get_cell(next_row,next_column,) != player:
                return False
        return True
    @staticmethod
    def _collect_direction(board,row,column,row_delta,column_delta,player,):
        cells = []
        for index in range(WIN_LENGTH):
            next_row = row + row_delta * index
            next_column = column + column_delta * index
            if not board.is_valid_position(next_row,next_column,):
                return []
            if board.get_cell(next_row,next_column,) != player:
                return []
            cells.append((next_row,next_column,))
        return cells