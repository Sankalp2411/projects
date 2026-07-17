#games/tic_tac_teo/board_renderer.py
from games.tic_tac_toe.constants import (BOARD_ROWS,BOARD_COLUMNS,CELL_SIZE,BOARD_PADDING,GRID_COLOR,X_COLOR,O_COLOR,EMPTY,PLAYER_X,PLAYER_O,WIN_LINE_COLOR,)
class BoardRenderer:
    def __init__(self, renderer):
        self.renderer = renderer
        self.origin_x = BOARD_PADDING
        self.origin_y = BOARD_PADDING
    def render(self, board,game_result=None,):
        self.draw_grid()
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                value = board.get_cell(row, column)
                if value == PLAYER_X:
                    self.draw_x(row, column)
                elif value == PLAYER_O:
                    self.draw_o(row, column)
        if (game_result is not None and game_result.winning_cells):
            self.draw_winning_line(game_result.winning_cells)
    def draw_grid(self):
        self.renderer.draw_grid(origin=(self.origin_x, self.origin_y),rows=BOARD_ROWS,columns=BOARD_COLUMNS,cell_size=CELL_SIZE,color=GRID_COLOR,)
    def draw_x(self, row, column):
        center = self.get_cell_center(row, column)
        self.renderer.draw_cross(center=center,size=CELL_SIZE * 0.60,color=X_COLOR,)
    def draw_o(self, row, column):
        center = self.get_cell_center(row, column)
        self.renderer.draw_circle(center=center,radius=CELL_SIZE * 0.30,color=O_COLOR,)
    def get_cell_center(self, row, column):
        x = (self.origin_x + column * CELL_SIZE + CELL_SIZE / 2)
        y = (self.origin_y + row * CELL_SIZE + CELL_SIZE / 2 )
        return (x, y)
    def contains_point(self, x, y):
        board_width = BOARD_COLUMNS * CELL_SIZE
        board_height = BOARD_ROWS * CELL_SIZE
        return (self.origin_x <= x < self.origin_x + board_width and self.origin_y <= y < self.origin_y + board_height)
    def screen_to_cell(self, x, y):
        if not self.contains_point(x, y):
            return None
        column = int((x - self.origin_x) // CELL_SIZE)
        row = int((y - self.origin_y) // CELL_SIZE)
        return (row, column)
    def draw_winning_line(self,winning_cells,):
        if len(winning_cells) < 2:
            return
        start = self.get_cell_center(*winning_cells[0])
        end = self.get_cell_center(*winning_cells[-1])
        self.renderer.draw_line(start=start,end=end,color=WIN_LINE_COLOR,)
    def reset(self):
        pass