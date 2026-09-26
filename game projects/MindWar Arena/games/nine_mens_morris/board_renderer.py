# games/nine_mens_morris/board_renderer.py
import math
from games.nine_mens_morris.constants import (BOARD_LEFT,BOARD_TOP,OUTER_SIZE,MIDDLE_SIZE,INNER_SIZE,STONE_RADIUS,POSITION_RADIUS,GRID_COLOR,POSITION_COLOR,PLAYER_BLACK,PLAYER_WHITE,PLAYER_BLACK_COLOR,PLAYER_WHITE_COLOR,SELECTED_COLOR,WIN_LINE_COLOR,POSITION_COORDINATES,)
class BoardRenderer:
    def __init__(self, renderer):
        self.renderer = renderer
        self.selected_position = None
    def render(self,board,game_result=None,selected_position=None,):
        self.selected_position = selected_position
        self.draw_board()
        for position in range(24):
            value = board.get_position(position)
            if value == PLAYER_BLACK:
                self.draw_stone(position,PLAYER_BLACK_COLOR,)
            elif value == PLAYER_WHITE:
                self.draw_stone(position,PLAYER_WHITE_COLOR,)
            else:
                self.draw_position(position)
        if ( game_result is not None and game_result.winning_cells):
            self.draw_winning_line(game_result.winning_cells)
        if selected_position is not None:
            self.draw_selection(selected_position)
    def draw_board(self):
        outer_left = BOARD_LEFT
        outer_top = BOARD_TOP
        outer_right = (BOARD_LEFT + OUTER_SIZE)
        outer_bottom = (BOARD_TOP + OUTER_SIZE)
        middle_offset = (OUTER_SIZE - MIDDLE_SIZE) / 2
        middle_left = (BOARD_LEFT + middle_offset)
        middle_top = (BOARD_TOP + middle_offset)
        middle_right = (middle_left + MIDDLE_SIZE)
        middle_bottom = (middle_top + MIDDLE_SIZE)
        inner_offset = (OUTER_SIZE - INNER_SIZE) / 2
        inner_left = (BOARD_LEFT + inner_offset)
        inner_top = (BOARD_TOP + inner_offset)
        inner_right = (inner_left + INNER_SIZE)
        inner_bottom = (inner_top + INNER_SIZE)
        center_x = (BOARD_LEFT + OUTER_SIZE / 2)
        center_y = (BOARD_TOP + OUTER_SIZE / 2)
        self.renderer.draw_rectangle(position=(outer_left,outer_top,),size=(OUTER_SIZE,OUTER_SIZE,),color=GRID_COLOR,)
        self.renderer.draw_rectangle(position=(middle_left,middle_top,),size=(MIDDLE_SIZE,MIDDLE_SIZE,),color=GRID_COLOR,)
        self.renderer.draw_rectangle(position=(inner_left,inner_top,),size=(INNER_SIZE,INNER_SIZE,),color=GRID_COLOR,)
        self.renderer.draw_line(start=(outer_left,center_y,),end=(inner_left,center_y,),color=GRID_COLOR,)
        self.renderer.draw_line(start=(inner_right,center_y,),end=(outer_right,center_y,),color=GRID_COLOR,)
        self.renderer.draw_line(start=(center_x,outer_top,),end=(center_x,inner_top,),color=GRID_COLOR,)
        self.renderer.draw_line(start=(center_x,inner_bottom,),end=(center_x,outer_bottom,),color=GRID_COLOR,)
    def draw_position(self, position):
        center = POSITION_COORDINATES[position]
        self.renderer.draw_filled_circle(center=center,radius=POSITION_RADIUS,color=POSITION_COLOR,)
    def draw_stone(self,position,color,):
        center = POSITION_COORDINATES[position]
        self.renderer.draw_filled_circle(center=center,radius=STONE_RADIUS,color=color,)
    def draw_selection(self, position):
        center = POSITION_COORDINATES[position]
        self.renderer.draw_circle(center=center,radius=STONE_RADIUS + 6,color=SELECTED_COLOR,)
    def draw_winning_line(self,winning_cells,):
        if len(winning_cells) < 2:
            return
        start = POSITION_COORDINATES[winning_cells[0]]
        end = POSITION_COORDINATES[winning_cells[-1]]
        self.renderer.draw_line(start=start,end=end,color=WIN_LINE_COLOR,)
    def contains_point(self, x, y):
        left = BOARD_LEFT
        top = BOARD_TOP
        right = (BOARD_LEFT + OUTER_SIZE)
        bottom = (BOARD_TOP + OUTER_SIZE)
        return (left - 25 <= x <= right + 25 and top - 25 <= y <= bottom + 25)
    def screen_to_position(self, x, y):
        if not self.contains_point(x, y):
            return None
        closest_position = None
        closest_distance = float("inf")
        for (position,coordinate,) in POSITION_COORDINATES.items():
            dx = (x - coordinate[0])
            dy = (y - coordinate[1])
            distance = math.sqrt(dx * dx + dy * dy)
            if (distance <= STONE_RADIUS + 15):
                if (distance < closest_distance):
                    closest_distance = distance
                    closest_position = position
        return closest_position
    def reset(self):
        self.selected_position = None