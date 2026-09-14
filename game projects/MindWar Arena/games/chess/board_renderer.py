# games/chess/board_renderer.py
from games.chess.constants import (BLACK_BISHOP,BLACK_KING,BLACK_KNIGHT,BLACK_PAWN,BLACK_QUEEN,BLACK_ROOK,BOARD_COLUMNS,BOARD_PADDING,BOARD_ROWS,CAPTURE_MOVE_COLOR,DARK_SQUARE_COLOR,EMPTY,KING_INDICATOR_RADIUS,LEGAL_MOVE_COLOR,LIGHT_SQUARE_COLOR,LAST_MOVE_COLOR,PIECE_OUTLINE_COLOR,PIECE_RADIUS,SELECTED_CELL_COLOR,WHITE_BISHOP,WHITE_KING,WHITE_KNIGHT,WHITE_PAWN,WHITE_QUEEN,WHITE_ROOK,)
class ChessBoardRenderer:
    def __init__(self, renderer):
        self.renderer = renderer
    def reset(self):
        pass
    def render(self,board,legal_moves=None,selected_position=None,last_move=None,check_position=None,en_passant_target=None,):
        if board is None:
            return
        legal_moves = legal_moves or []
        self._draw_board()
        self._draw_last_move(last_move)
        self._draw_highlights(board,legal_moves,selected_position,en_passant_target,)
        self._draw_check(check_position)
        self._draw_pieces(board)
    def board_to_screen(self,row,column,):
        if not (0 <= row < BOARD_ROWS and 0 <= column < BOARD_COLUMNS):
            raise ValueError(f"Invalid board position: "f"({row}, {column})")
        cell_size = self._get_cell_size()
        x = (BOARD_PADDING + (column + 0.5) * cell_size)
        y = (BOARD_PADDING + (row + 0.5) * cell_size)
        return x, y
    def screen_to_board(self,position,):
        if position is None:
            return None
        if not isinstance(position,(tuple, list),):
            return None
        if len(position) != 2:
            return None
        x, y = position
        if not (isinstance(x, (int, float)) and isinstance(y, (int, float))):
            return None
        cell_size = self._get_cell_size()
        board_x = (x - BOARD_PADDING)
        board_y = (y - BOARD_PADDING)
        if board_x < 0 or board_y < 0:
            return None
        board_pixel_size = (self._board_pixel_size())
        if (board_x >= board_pixel_size or board_y >= board_pixel_size):
            return None
        column = int(board_x // cell_size)
        row = int(board_y // cell_size)
        if not (0 <= row < BOARD_ROWS and 0 <= column < BOARD_COLUMNS):
            return None
        return row, column
    def get_board_size(self):
        size = (self._board_pixel_size() + BOARD_PADDING * 2)
        return size, size
    def _draw_board(self):
        cell_size = self._get_cell_size()
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                if (row + column) % 2 == 0:
                    square_color = (LIGHT_SQUARE_COLOR)
                else:
                    square_color = (DARK_SQUARE_COLOR)
                left = (BOARD_PADDING + column * cell_size)
                top = (BOARD_PADDING + row * cell_size)
                self._draw_filled_rectangle(left,top,cell_size,cell_size,square_color,)
    def _draw_pieces(self,board,):
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                piece = board.get_cell(row,column,)
                if piece == EMPTY:
                    continue
                center = self.board_to_screen(row,column,)
                self._draw_piece(center,piece,)
    def _draw_piece(self,center,piece,):
        if piece in (WHITE_PAWN,WHITE_KNIGHT,WHITE_BISHOP,WHITE_ROOK,WHITE_QUEEN,WHITE_KING,):
            piece_color = (245,245,245,)
            outline_color = (PIECE_OUTLINE_COLOR)
            text_color = (30,30,30,)
        elif piece in (BLACK_PAWN,BLACK_KNIGHT,BLACK_BISHOP,BLACK_ROOK,BLACK_QUEEN,BLACK_KING,):
            piece_color = (35,35,35,)
            outline_color = (220,220,220,)
            text_color = (245,245,245,)
        else:
            return
        self.renderer.draw_filled_circle(center,PIECE_RADIUS,piece_color,)
        self.renderer.draw_circle(center,PIECE_RADIUS,outline_color,32,)
        if piece in (WHITE_KING,BLACK_KING,):
            self.renderer.draw_circle(center,KING_INDICATOR_RADIUS,outline_color,32,)
        symbol = self._get_piece_symbol(piece)
        text_size = 28
        self._draw_centered_text(symbol,center,text_size,text_color,)
    @staticmethod
    def _get_piece_symbol(piece,):
        symbols = {WHITE_PAWN: "P",WHITE_KNIGHT: "N",WHITE_BISHOP: "B",WHITE_ROOK: "R",WHITE_QUEEN: "Q",WHITE_KING: "K",BLACK_PAWN: "p",BLACK_KNIGHT: "n",BLACK_BISHOP: "b",BLACK_ROOK: "r",BLACK_QUEEN: "q",BLACK_KING: "k",}
        return symbols.get(piece,"",)
    def _draw_centered_text(self,text,center,size,color,):
        x = center[0] - size * 0.30
        y = center[1] - size * 0.50
        self.renderer.draw_text(text,(x, y),size=size,color=color,)
    def _draw_highlights(self,board,legal_moves,selected_position,en_passant_target,):
        if selected_position is not None:
            self._draw_cell_highlight(selected_position,SELECTED_CELL_COLOR,)
        destinations = {}
        for move in legal_moves:
            if not isinstance(move,(tuple, list),):
                continue
            if len(move) not in (4,5,):
                continue
            destination = (move[2],move[3],)
            is_capture = (self._is_capture_move(board,move,en_passant_target,))
            if destination not in destinations:
                destinations[destination] = is_capture
            elif is_capture:
                destinations[destination] = True
        for (destination,is_capture,) in destinations.items():
            if is_capture:
                color = (CAPTURE_MOVE_COLOR)
            else:
                color = (LEGAL_MOVE_COLOR)
            self._draw_destination_highlight(destination,color,)
    def _draw_cell_highlight(self,position,color,):
        if position is None:
            return
        if not isinstance(position,(tuple, list),):
            return
        if len(position) != 2:
            return
        row, column = position
        if not (0 <= row < BOARD_ROWS and 0 <= column < BOARD_COLUMNS):
            return
        cell_size = self._get_cell_size()
        left = (BOARD_PADDING + column * cell_size)
        top = (BOARD_PADDING + row * cell_size)
        self._draw_rectangle_outline(left,top,cell_size,cell_size,color,4,)
    def _draw_destination_highlight(self,position,color,):
        if position is None:
            return
        row, column = position
        if not (0 <= row < BOARD_ROWS and 0 <= column < BOARD_COLUMNS):
            return
        center = self.board_to_screen(row,column,)
        radius = (self._get_cell_size() * 0.13)
        self.renderer.draw_filled_circle(center,radius,color,)
    def _draw_last_move(self,last_move,):
        if not isinstance(last_move,(tuple, list),):
            return
        if len(last_move) not in (4,5,):
            return
        from_position = (last_move[0],last_move[1],)
        to_position = (last_move[2],last_move[3],)
        self._draw_cell_highlight(from_position,LAST_MOVE_COLOR,)
        self._draw_cell_highlight(to_position,LAST_MOVE_COLOR,)
    def _draw_check(self,check_position,):
        if check_position is None:
            return
        if not isinstance(check_position,(tuple, list),):
            return
        if len(check_position) != 2:
            return
        row, column = check_position
        if not (0 <= row < BOARD_ROWS and 0 <= column < BOARD_COLUMNS):
            return
        center = self.board_to_screen(row,column,)
        radius = (self._get_cell_size() * 0.30)
        self.renderer.draw_circle(center,radius,(255, 80, 80),32,)
    @staticmethod
    def _is_capture_move(board,move,en_passant_target=None,):
        if board is None:
            return False
        if not isinstance(move,(tuple, list),):
            return False
        if len(move) not in (4,5,):
            return False
        from_row = move[0]
        from_column = move[1]
        to_row = move[2]
        to_column = move[3]
        if not (0 <= from_row < BOARD_ROWS and 0 <= from_column < BOARD_COLUMNS and 0 <= to_row < BOARD_ROWS and 0 <= to_column < BOARD_COLUMNS):
            return False
        moving_piece = board.get_cell(from_row,from_column,)
        destination_piece = board.get_cell(to_row,to_column,)
        if destination_piece != EMPTY:
            return True
        if (en_passant_target is not None and ChessBoardRenderer._is_pawn(moving_piece)):
            if ((to_row, to_column) == en_passant_target):
                return (from_column != to_column and destination_piece == EMPTY)
        return False
    @staticmethod
    def _is_pawn(piece,):
        return piece in (WHITE_PAWN,BLACK_PAWN,)
    def _draw_filled_rectangle(self,x,y,width,height,color,):
        self.renderer.draw_filled_rectangle((x, y),(width, height),color,)
    def _draw_rectangle_outline(self,x,y,width,height,color,line_width,):
        self.renderer.draw_rectangle((x, y),(width, height),color,)
    def _get_cell_size(self):
        return (self._board_pixel_size() / BOARD_COLUMNS)
    def _board_pixel_size(self):
        return 560.0