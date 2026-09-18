#games/go/board_renderer.py
from games.go.constants import (BOARD_COLUMNS,BOARD_COLOR,BOARD_LINE_WIDTH,BOARD_PADDING,BOARD_ROWS,CELL_SIZE,GRID_COLOR,KO_COLOR,LAST_MOVE_COLOR,LEGAL_MOVE_COLOR,PLAYER_BLACK,PLAYER_BLACK_COLOR,PLAYER_WHITE,PLAYER_WHITE_COLOR,STAR_POINTS,STONE_RADIUS,)
class GoBoardRenderer:
    def __init__(self, renderer):
        self.renderer = renderer
        self.origin_x = BOARD_PADDING
        self.origin_y = BOARD_PADDING
    def reset(self):
        pass
    def render(self,board,legal_moves=None,last_move=None,ko_position=None,):
        self._render_board()
        self._render_star_points()
        self._render_stones(board)
        if legal_moves:
            self.render_legal_moves(legal_moves)
        self.render_last_move(last_move)
        self.render_ko_position(ko_position)
    def _render_board(self):
        board_width = ((BOARD_COLUMNS - 1) * CELL_SIZE)
        board_height = ((BOARD_ROWS - 1) * CELL_SIZE)
        half_cell = CELL_SIZE / 2
        self.renderer.draw_filled_rectangle(
            (self.origin_x - half_cell,self.origin_y - half_cell,),(board_width + CELL_SIZE,board_height + CELL_SIZE,),BOARD_COLOR,)
        for row in range(BOARD_ROWS):
            y = (self.origin_y + row * CELL_SIZE)
            self.renderer.draw_line((self.origin_x,y,),(self.origin_x + board_width,y,),GRID_COLOR,)
        for column in range(BOARD_COLUMNS):
            x = (self.origin_x + column * CELL_SIZE)
            self.renderer.draw_line((x,self.origin_y,),(x,self.origin_y + board_height,),GRID_COLOR,)
    def _render_star_points(self):
        for row, column in STAR_POINTS:
            center = self.get_cell_center(row,column,)
            self.renderer.draw_filled_circle(center,CELL_SIZE * 0.07,GRID_COLOR,)
    def _render_stones(self, board):
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                cell = board.get_cell(row,column,)
                if cell == PLAYER_BLACK:
                    color = PLAYER_BLACK_COLOR
                elif cell == PLAYER_WHITE:
                    color = PLAYER_WHITE_COLOR
                else:
                    continue
                center = self.get_cell_center(row,column,)
                self.renderer.draw_filled_circle(center,STONE_RADIUS,color,)
    def render_legal_moves(self, legal_moves):
        if not legal_moves:
            return
        indicator_radius = (STONE_RADIUS * 0.20)
        for row, column in legal_moves:
            center = self.get_cell_center(row,column,)
            self.renderer.draw_filled_circle(center,indicator_radius,LEGAL_MOVE_COLOR,)
    def render_last_move(self, move):
        if move is None:
            return
        if not isinstance(move, tuple):
            return
        if len(move) != 2:
            return
        row, column = move
        center = self.get_cell_center(row,column,)
        self.renderer.draw_filled_circle(center,STONE_RADIUS * 0.10,LAST_MOVE_COLOR,)
    def render_ko_position(self, position):
        if position is None:
            return
        if not isinstance(position, tuple):
            return
        if len(position) != 2:
            return
        row, column = position
        center = self.get_cell_center(row,column,)
        self.renderer.draw_filled_circle(center,STONE_RADIUS * 0.18,KO_COLOR,)
    def get_cell_center(self, row, column):
        if not 0 <= row < BOARD_ROWS:
            raise ValueError(f"Invalid row: {row}")
        if not 0 <= column < BOARD_COLUMNS:
            raise ValueError(f"Invalid column: {column}")
        x = (self.origin_x + column * CELL_SIZE)
        y = (self.origin_y + row * CELL_SIZE)
        return (x, y)
    def contains_point(self, x, y):
        board_width = ((BOARD_COLUMNS - 1) * CELL_SIZE)
        board_height = ((BOARD_ROWS - 1) * CELL_SIZE)
        half_cell = CELL_SIZE / 2
        return ( self.origin_x - half_cell <= x <= self.origin_x + board_width + half_cell and self.origin_y - half_cell <= y <= self.origin_y + board_height + half_cell)
    def screen_to_board(self, position):
        if position is None:
            return None
        x, y = position
        if not self.contains_point(x, y):
            return None
        column = round(
            (x - self.origin_x) / CELL_SIZE)
        row = round((y - self.origin_y) / CELL_SIZE)
        if not (0 <= row < BOARD_ROWS and 0 <= column < BOARD_COLUMNS):
            return None
        return (row, column)
    def screen_to_cell(self, x, y):
        return self.screen_to_board((x, y))