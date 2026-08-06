from engine.interfaces.game_result import GameResult

from games.connect4.constants import (
    BOARD_ROWS,
    BOARD_COLUMNS,
    WIN_LENGTH,
    EMPTY,
    NO_WINNER,
)


class Connect4Rules:

    _DIRECTIONS = (
        (0, 1),     # Horizontal
        (1, 0),     # Vertical
        (1, 1),     # Diagonal down-right
        (-1, 1),    # Diagonal up-right
    )

    @staticmethod
    def check_winner(board):
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):

                player = board.get_cell(row, column)

                if player == EMPTY:
                    continue

                for row_delta, column_delta in Connect4Rules._DIRECTIONS:

                    if Connect4Rules._check_direction(
                        board,
                        row,
                        column,
                        row_delta,
                        column_delta,
                        player,
                    ):
                        return player

        return NO_WINNER

    @staticmethod
    def get_winning_cells(board):
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):

                player = board.get_cell(row, column)

                if player == EMPTY:
                    continue

                for row_delta, column_delta in Connect4Rules._DIRECTIONS:

                    cells = Connect4Rules._collect_direction(
                        board,
                        row,
                        column,
                        row_delta,
                        column_delta,
                        player,
                    )

                    if cells:
                        return cells

        return []

    @staticmethod
    def is_draw(board):
        return (
            Connect4Rules.check_winner(board) == NO_WINNER
            and board.is_board_full()
        )

    @staticmethod
    def is_game_over(board):
        return (
            Connect4Rules.check_winner(board) != NO_WINNER
            or board.is_board_full()
        )

    @staticmethod
    def evaluate_game(board):
        result = GameResult()

        winner = Connect4Rules.check_winner(board)

        if winner != NO_WINNER:
            result.winner = winner
            result.game_over = True
            result.winning_cells = Connect4Rules.get_winning_cells(board)
            return result

        if board.is_board_full():
            result.draw = True
            result.game_over = True

        return result

    @staticmethod
    def _check_direction(
        board,
        row,
        column,
        row_delta,
        column_delta,
        player,
    ):
        for index in range(1, WIN_LENGTH):

            next_row = row + row_delta * index
            next_column = column + column_delta * index

            if not board.is_valid_position(next_row, next_column):
                return False

            if board.get_cell(next_row, next_column) != player:
                return False

        return True

    @staticmethod
    def _collect_direction(
        board,
        row,
        column,
        row_delta,
        column_delta,
        player,
    ):
        cells = []

        for index in range(WIN_LENGTH):

            next_row = row + row_delta * index
            next_column = column + column_delta * index

            if not board.is_valid_position(next_row, next_column):
                return []

            if board.get_cell(next_row, next_column) != player:
                return []

            cells.append((next_row, next_column))

        return cells