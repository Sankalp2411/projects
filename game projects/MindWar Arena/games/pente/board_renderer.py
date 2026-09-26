# games/pente/board_renderer.py
from games.pente.constants import (BOARD_ROWS,BOARD_COLUMNS,CELL_SIZE,BOARD_PADDING,GRID_COLOR,PLAYER_BLACK,PLAYER_WHITE,PLAYER_BLACK_COLOR,PLAYER_WHITE_COLOR,STONE_RADIUS,WIN_LINE_COLOR,)
class BoardRenderer:
    def __init__(self, renderer):
        self.renderer = renderer
        self.origin_x = BOARD_PADDING
        self.origin_y = BOARD_PADDING
    def render(self, board, game_result=None):
        self.draw_grid()
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                value = board.get_cell(row,column,)
                if value == PLAYER_BLACK:
                    self.draw_stone(row,column,PLAYER_BLACK_COLOR,)
                elif value == PLAYER_WHITE:
                    self.draw_stone(row,column,PLAYER_WHITE_COLOR,)
        if (game_result is not None and game_result.winning_cells):
            self.draw_winning_line(game_result.winning_cells)
    def draw_grid(self):
        self.renderer.draw_grid(origin=(self.origin_x,self.origin_y,),rows=BOARD_ROWS,columns=BOARD_COLUMNS,cell_size=CELL_SIZE,color=GRID_COLOR,)
    def draw_stone(self, row, column, color):
        center = self.get_cell_center(row,column,)
        self.renderer.draw_circle(center=center,radius=STONE_RADIUS,color=color,)
    def get_cell_center(self, row, column):
        x = (self.origin_x + column * CELL_SIZE)
        y = (self.origin_y + row * CELL_SIZE)
        return (x, y)
    def contains_point(self, x, y):
        board_width = ((BOARD_COLUMNS - 1) * CELL_SIZE)
        board_height = ((BOARD_ROWS - 1) * CELL_SIZE)
        return (self.origin_x <= x <= self.origin_x + board_width and self.origin_y <= y <= self.origin_y + board_height)
    def screen_to_cell(self, x, y):
        if not self.contains_point(x, y):
            return None
        column = round((x - self.origin_x) / CELL_SIZE)
        row = round((y - self.origin_y) / CELL_SIZE)
        if not (0 <= row < BOARD_ROWS and 0 <= column < BOARD_COLUMNS):
            return None
        return (row,column,)
    def draw_winning_line(self, winning_cells):
        if len(winning_cells) < 2:
            return
        start = self.get_cell_center(*winning_cells[0])
        end = self.get_cell_center(*winning_cells[-1])
        self.renderer.draw_line(start=start,end=end,color=WIN_LINE_COLOR,)
    def reset(self):
        pass