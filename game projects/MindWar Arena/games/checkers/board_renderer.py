# games/checkers/board_renderer.py
from games.checkers.constants import (BOARD_COLUMNS,BOARD_PADDING,BOARD_ROWS,CAPTURE_MOVE_COLOR,DARK_SQUARE_COLOR,EMPTY,KING_INDICATOR_COLOR,KING_INDICATOR_RADIUS,LEGAL_MOVE_COLOR,LIGHT_SQUARE_COLOR,PIECE_RADIUS,BLACK_KING,BLACK_MAN,PLAYER_BLACK,PLAYER_WHITE,SELECTED_CELL_COLOR,WHITE_KING,WHITE_MAN,)
class CheckersBoardRenderer:
    def __init__(self, renderer):
        self.renderer = renderer
    def reset(self):
        pass
    def render(self,board,legal_moves=None,selected_position=None,active_capture_piece=None,):
        self._draw_board()
        self._draw_highlights(legal_moves or [],selected_position,active_capture_piece,)
        self._draw_pieces(board)
    def board_to_screen(self, row, column):
        if not (0 <= row < BOARD_ROWS and 0 <= column < BOARD_COLUMNS):
            raise ValueError(f"Invalid board position: ({row}, {column})")
        cell_size = self._get_cell_size()
        x = (BOARD_PADDING + (column + 0.5) * cell_size)
        y = (BOARD_PADDING + (row + 0.5) * cell_size)
        return x, y
    def screen_to_board(self, position):
        if position is None:
            return None
        x, y = position
        cell_size = self._get_cell_size()
        board_x = x - BOARD_PADDING
        board_y = y - BOARD_PADDING
        if board_x < 0 or board_y < 0:
            return None
        column = int(board_x // cell_size)
        row = int(board_y // cell_size)
        if not (0 <= row < BOARD_ROWS and 0 <= column < BOARD_COLUMNS):
            return None
        return row, column
    def get_board_size(self):
        size = (BOARD_COLUMNS * self._get_cell_size() + BOARD_PADDING * 2)
        return size, size
    def _draw_board(self):
        cell_size = self._get_cell_size()
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                if (row + column) % 2 == 1:
                    square_color = DARK_SQUARE_COLOR
                else:
                    square_color = LIGHT_SQUARE_COLOR
                left = (BOARD_PADDING + column * cell_size)
                top = (BOARD_PADDING + row * cell_size)
                self._draw_rectangle(left,top,cell_size,cell_size,square_color,)
    def _draw_pieces(self, board):
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                piece = board.get_cell(row,column,)
                if piece == EMPTY:
                    continue
                center = self.board_to_screen(row,column,)
                self._draw_piece(center,piece,)
    def _draw_piece(self, center, piece):
        if piece in (BLACK_MAN,BLACK_KING,):
            piece_color = (30,30,30,)
        elif piece in (WHITE_MAN,WHITE_KING,):
            piece_color = (235,235,235,)
        else:
            return
        self.renderer.draw_filled_circle(center,PIECE_RADIUS,piece_color,)
        if piece in (WHITE_MAN,WHITE_KING,):
            self.renderer.draw_circle(center,PIECE_RADIUS,(40, 40, 40),2,)
        if piece in (BLACK_KING,WHITE_KING,):
            self.renderer.draw_filled_circle(center,KING_INDICATOR_RADIUS,KING_INDICATOR_COLOR,)
    def _draw_highlights(self,legal_moves,selected_position,active_capture_piece,):
        if selected_position is not None:
            self._draw_cell_highlight(selected_position,SELECTED_CELL_COLOR,)
        if active_capture_piece is not None:
            self._draw_cell_highlight(active_capture_piece,SELECTED_CELL_COLOR,)
        destinations = set()
        for move in legal_moves:
            if not isinstance(move,(tuple, list),):
                continue
            if len(move) != 4:
                continue
            destination = (move[2],move[3],)
            destinations.add((destination,self._is_capture_move(move),))
        for destination, is_capture in destinations:
            if is_capture:
                color = CAPTURE_MOVE_COLOR
            else:
                color = LEGAL_MOVE_COLOR
            self._draw_destination_highlight(destination,color,)
    def _draw_cell_highlight(self,position,color,):
        row, column = position
        if not (0 <= row < BOARD_ROWS and 0 <= column < BOARD_COLUMNS):
            return
        cell_size = self._get_cell_size()
        left = (BOARD_PADDING + column * cell_size)
        top = (BOARD_PADDING + row * cell_size)
        self._draw_rectangle_outline(left,top,cell_size,cell_size,color,4,)
    def _draw_destination_highlight(self,position,color,):
        row, column = position
        if not (0 <= row < BOARD_ROWS and 0 <= column < BOARD_COLUMNS):
            return
        center = self.board_to_screen(row,column,)
        radius = (self._get_cell_size() * 0.13) 
        self.renderer.draw_filled_circle(center,radius,color,)
    @staticmethod
    def _is_capture_move(move):
        return (abs(move[2] - move[0]) == 2 and abs(move[3] - move[1]) == 2)
    def _draw_rectangle(self,x,y,width,height,color,):
        self.renderer.draw_rectangle((x, y),(width, height),color,)
    def _draw_rectangle_outline(self,x,y,width,height,color,line_width,):
        if hasattr(self.renderer,"draw_rectangle_outline",):
            self.renderer.draw_rectangle_outline((x, y),(width, height),color,line_width,)
            return
        if hasattr(self.renderer,"draw_rectangle",):
            self.renderer.draw_rectangle((x, y),(width, height),color,)
    def _get_cell_size(self):
        return (self._board_pixel_size() / BOARD_COLUMNS)
    def _board_pixel_size(self):
        return 560.0