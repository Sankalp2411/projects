#games/go/rules.py
from engine.interfaces.game_result import GameResult
from games.go.constants import (BOARD_ROWS,BOARD_COLUMNS,EMPTY,PLAYER_BLACK,PLAYER_WHITE,GAME_NOT_STARTED,GAME_RUNNING,GAME_DRAW,GAME_OVER,NO_WINNER,KOMI,)
class GoRules:
    @staticmethod
    def get_opponent(player):
        if player == PLAYER_BLACK:
            return PLAYER_WHITE
        if player == PLAYER_WHITE:
            return PLAYER_BLACK
        return None
    @staticmethod
    def is_valid_player(player):
        return player in (PLAYER_BLACK, PLAYER_WHITE)
    @staticmethod
    def is_valid_position(row, column):
        return (isinstance(row, int) and isinstance(column, int) and 0 <= row < BOARD_ROWS and 0 <= column < BOARD_COLUMNS)
    @staticmethod
    def is_same_position(position_a, position_b):
        return position_a == position_b
    @classmethod
    def get_neighbors(cls, row, column):
        if not cls.is_valid_position(row, column):
            return []
        neighbors = []
        directions = ((-1, 0),(1, 0),(0, -1),(0, 1),)
        for delta_row, delta_column in directions:
            neighbor_row = row + delta_row
            neighbor_column = column + delta_column
            if cls.is_valid_position(neighbor_row,neighbor_column,):
                neighbors.append((neighbor_row,neighbor_column,))
        return neighbors
    @classmethod
    def get_group(cls, board, row, column):
        if board is None:
            return set()
        if not cls.is_valid_position(row, column):
            return set()
        player = board.get_cell(row, column)
        if player not in (PLAYER_BLACK, PLAYER_WHITE):
            return set()
        group = set()
        stack = [(row, column)]
        while stack:
            current = stack.pop()
            if current in group:
                continue
            current_row, current_column = current
            if not cls.is_valid_position(current_row,current_column,):
                continue
            if board.get_cell(current_row,current_column,) != player:
                continue
            group.add(current)
            for neighbor in cls.get_neighbors(current_row,current_column,):
                if neighbor not in group:
                    stack.append(neighbor)
        return group
    @classmethod
    def get_group_liberties(cls, board, group):
        if board is None:
            return set()
        if not group:
            return set()
        liberties = set()
        for row, column in group:
            for neighbor in cls.get_neighbors(row,column,):
                neighbor_row, neighbor_column = neighbor
                if board.get_cell(neighbor_row,neighbor_column,) == EMPTY:
                    liberties.add(neighbor)
        return liberties
    @classmethod
    def get_liberties(cls, board, row, column):
        group = cls.get_group(board,row,column,)
        return cls.get_group_liberties(board,group,)
    @classmethod
    def count_liberties(cls, board, row, column):
        return len(cls.get_liberties(board,row,column,))
    @classmethod
    def is_group_captured(cls, board, row, column):
        if board is None:
            return False
        if not cls.is_valid_position(row, column):
            return False
        player = board.get_cell(row, column)
        if player not in (PLAYER_BLACK, PLAYER_WHITE):
            return False
        group = cls.get_group(board,row,column,)
        liberties = cls.get_group_liberties(board,group,)
        return len(liberties) == 0
    @classmethod
    def get_captured_positions(cls,board,player,row,column,):
        if board is None:
            return set()
        if not cls.is_valid_player(player):
            return set()
        if not cls.is_valid_position(row, column):
            return set()
        if not board.is_cell_empty(row, column):
            return set()
        opponent = cls.get_opponent(player)
        simulated_board = board.copy()
        if not simulated_board.place_stone(row,column,player,):
            return set()
        captured_positions = set()
        for neighbor in cls.get_neighbors(row,column,):
            neighbor_row, neighbor_column = neighbor
            if simulated_board.get_cell(neighbor_row,neighbor_column,) != opponent:
                continue
            group = cls.get_group(simulated_board,neighbor_row,neighbor_column,)
            liberties = cls.get_group_liberties(simulated_board,group,)
            if not liberties:
                captured_positions.update(group)
        return captured_positions
    @classmethod
    def capture_group(cls, board, row, column):
        if board is None:
            return 0
        if not cls.is_valid_position(row, column):
            return 0
        player = board.get_cell(row, column)
        if player not in (PLAYER_BLACK, PLAYER_WHITE):
            return 0
        group = cls.get_group(board,row,column,)
        liberties = cls.get_group_liberties(board,group,)
        if liberties:
            return 0
        removed = 0
        for group_row, group_column in group:
            if board.remove_stone(group_row,group_column,):
                removed += 1
        return removed
    @classmethod
    def capture_opponent_groups(cls,board,player,row,column,):
        if board is None:
            return 0
        if not cls.is_valid_player(player):
            return 0
        opponent = cls.get_opponent(player)
        captured_positions = set()
        for neighbor in cls.get_neighbors(row,column,):
            neighbor_row, neighbor_column = neighbor
            if board.get_cell(neighbor_row,neighbor_column,) != opponent:
                continue
            group = cls.get_group(board,neighbor_row,neighbor_column,)
            liberties = cls.get_group_liberties(board,group,)
            if not liberties:
                captured_positions.update(group)
        removed = 0
        for captured_row, captured_column in captured_positions:
            if board.remove_stone(captured_row,captured_column,):
                removed += 1
        return removed
    @classmethod
    def is_suicide(cls,board,row,column,player,):
        if board is None:
            return False
        if not cls.is_valid_player(player):
            return False
        if not cls.is_valid_position(row, column):
            return False
        if not board.is_cell_empty(row, column):
            return False
        simulated_board = board.copy()
        if not simulated_board.place_stone(row,column,player,):
            return False
        cls.capture_opponent_groups(simulated_board,player,row,column,)
        group = cls.get_group(simulated_board,row,column,)
        liberties = cls.get_group_liberties(simulated_board,group,)
        return len(liberties) == 0
    @classmethod
    def is_valid_move(cls,board,row,column,player,ko_position=None,):
        if board is None:
            return False
        if not cls.is_valid_player(player):
            return False
        if not cls.is_valid_position(row, column):
            return False
        if not board.is_cell_empty(row, column):
            return False
        position = (row, column)
        if ko_position is not None:
            if position == ko_position:
                return False
        captured_positions = cls.get_captured_positions(board,player,row,column,)
        if captured_positions:
            return True
        if cls.is_suicide(board,row,column,player,):
            return False
        return True
    @classmethod
    def get_valid_moves(cls,board,player,ko_position=None,):
        if board is None:
            return []
        if not cls.is_valid_player(player):
            return []
        moves = []
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                if cls.is_valid_move(board,row,column,player,ko_position,):
                    moves.append((row,column,))
        return moves
    @classmethod
    def get_legal_moves(cls,board,player,ko_position=None,):
        return cls.get_valid_moves(board,player,ko_position,)
    @classmethod
    def simulate_move(cls,board,row,column,player,ko_position=None,):
        if board is None:
            return None
        if not cls.is_valid_move(board,row,column,player,ko_position,):
            return None
        simulated_board = board.copy()
        if not simulated_board.place_stone(row,column,player,):
            return None
        cls.capture_opponent_groups(simulated_board,player,row,column,)
        return simulated_board
    @classmethod
    def apply_move(cls,board,row,column,player,ko_position=None,):
        if board is None:
            return False
        if not cls.is_valid_move(board,row,column,player,ko_position,):
            return False
        if not board.place_stone(row,column,player,):
            return False
        cls.capture_opponent_groups(board,player,row,column,)
        return True
    @classmethod
    def get_ko_position(cls,previous_board,current_board,move_row,move_column,player,):
        if previous_board is None or current_board is None:
            return None
        if not cls.is_valid_player(player):
            return None
        if not cls.is_valid_position(move_row,move_column,):
            return None
        opponent = cls.get_opponent(player)
        previous_opponent_positions = set(previous_board.get_player_positions(opponent))
        current_opponent_positions = set(current_board.get_player_positions(opponent))
        captured_positions = (previous_opponent_positions - current_opponent_positions)
        if len(captured_positions) != 1:
            return None
        captured_position = next(iter(captured_positions))
        current_player_positions = set(current_board.get_player_positions(player))
        previous_player_positions = set(previous_board.get_player_positions(player))
        new_player_positions = (current_player_positions - previous_player_positions)
        if len(new_player_positions) != 1:
            return None
        new_position = next(iter(new_player_positions))
        if new_position != (move_row,move_column,):
            return None
        recapture_board = current_board.copy()
        recapture_row, recapture_column = (captured_position)
        if not recapture_board.is_cell_empty(recapture_row,recapture_column,):
            return None
        if not cls.is_valid_move(recapture_board,recapture_row,recapture_column,opponent,None,):
            return None
        if not cls.apply_move(recapture_board,recapture_row,recapture_column,opponent,None,):
            return None
        if (recapture_board.get_board_state() == previous_board.get_board_state()):
            return captured_position
        return None
    @classmethod
    def is_ko_move(cls,previous_board,current_board,move_row,move_column,player,):
        return (
            cls.get_ko_position(previous_board,current_board,move_row,move_column,player,) is not None)
    @staticmethod
    def boards_equal(board_a, board_b):
        if board_a is None or board_b is None:
            return board_a is board_b
        return (board_a.get_board_state() == board_b.get_board_state())
    @classmethod
    def get_empty_regions(cls, board):
        if board is None:
            return []
        regions = []
        visited = set()
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                position = (row, column)
                if position in visited:
                    continue
                if board.get_cell(row,column,) != EMPTY:
                    continue
                region = set()
                stack = [position]
                while stack:
                    current = stack.pop()
                    if current in region:
                        continue
                    current_row, current_column = current
                    if board.get_cell(current_row,current_column,) != EMPTY:
                        continue
                    region.add(current)
                    visited.add(current)
                    for neighbor in cls.get_neighbors(current_row,current_column,):
                        if neighbor in region:
                            continue
                        neighbor_row, neighbor_column = neighbor
                        if board.get_cell(neighbor_row,neighbor_column,) == EMPTY:
                            stack.append(neighbor)
                if region:
                    regions.append(region)
        return regions
    @classmethod
    def get_region_owner(cls,board,region,):
        if board is None:
            return None
        if not region:
            return None
        for row, column in region:
            if (row == 0 or row == BOARD_ROWS - 1 or column == 0 or column == BOARD_COLUMNS - 1):
                return None
        bordering_players = set()
        for row, column in region:
            for neighbor in cls.get_neighbors(row,column,):
                neighbor_row, neighbor_column = neighbor
                value = board.get_cell(neighbor_row,neighbor_column,)
                if value in (PLAYER_BLACK,PLAYER_WHITE,):
                    bordering_players.add(value)
        if len(bordering_players) != 1:
            return None
        return next(iter(bordering_players))
    @classmethod
    def count_territory(cls,board,player,):
        if board is None:
            return 0
        if not cls.is_valid_player(player):
            return 0
        territory = 0
        regions = cls.get_empty_regions(board)
        for region in regions:
            owner = cls.get_region_owner(board,region,)
            if owner == player:
                territory += len(region)
        return territory
    @classmethod
    def calculate_score(cls,board,player,):
        if board is None:
            return 0.0
        if not cls.is_valid_player(player):
            return 0.0
        stone_count = board.count_stones(player)
        territory_count = cls.count_territory(board,player,)
        score = (stone_count + territory_count)
        if player == PLAYER_WHITE:
            score += KOMI
        return float(score)
    @classmethod
    def get_scores(cls, board):
        return {PLAYER_BLACK: cls.calculate_score(board,PLAYER_BLACK,),PLAYER_WHITE: cls.calculate_score(board,PLAYER_WHITE,),}
    @classmethod
    def get_winner(cls, board):
        scores = cls.get_scores(board)
        black_score = scores[PLAYER_BLACK]
        white_score = scores[PLAYER_WHITE]
        if black_score > white_score:
            return PLAYER_BLACK
        if white_score > black_score:
            return PLAYER_WHITE
        return None
    @classmethod
    def is_draw(cls, board):
        scores = cls.get_scores(board)
        return (scores[PLAYER_BLACK] == scores[PLAYER_WHITE])
    @classmethod
    def evaluate_game(cls, board):
        result = GameResult()
        if board is None:
            return result
        scores = cls.get_scores(board)
        result.scores = scores
        result.game_over = True
        black_score = scores[PLAYER_BLACK]
        white_score = scores[PLAYER_WHITE]
        if black_score > white_score:
            result.winner = PLAYER_BLACK
            result.draw = False
        elif white_score > black_score:
            result.winner = PLAYER_WHITE
            result.draw = False
        else:
            result.winner = None
            result.draw = True
        return result
    @classmethod
    def has_legal_moves(cls,board,player,ko_position=None,):
        return bool(cls.get_legal_moves(board,player,ko_position,))
    @classmethod
    def is_board_full(cls, board):
        if board is None:
            return False
        return board.is_board_full()
    @classmethod
    def get_stone_count(cls, board, player):
        if board is None:
            return 0
        if not cls.is_valid_player(player):
            return 0
        return board.count_stones(player)
    @classmethod
    def get_position_count(cls, board, player):
        return cls.get_stone_count(board,player,)