# games/othello/overlay_renderer.py
from games.othello.constants import (GAME_DRAW,GAME_OVER,PLAYER_BLACK,PLAYER_WHITE,)
class OthelloOverlayRenderer:
    def __init__(self):
        self.message = ""
        self.visible = False
    def render(self, renderer, result, board):
        if result is None:
            return
        if not result.game_over:
            return
        message = self._get_game_over_message(result,board,)
        if not message:
            return
        renderer.draw_overlay_message(message)
    def _get_game_over_message(self, result, board):
        black_count = board.count_stones(PLAYER_BLACK)
        white_count = board.count_stones(PLAYER_WHITE)
        if result.draw:
            return (f"Draw-Black:{black_count}"f"White:{white_count}")
        if result.winner == PLAYER_BLACK:
            return (f"Black Wins-Black:{black_count}"f"White:{white_count}")
        if result.winner == PLAYER_WHITE:
            return (f"White Wins-Black:{black_count}"f"White:{white_count}")
        return (f"Game Over-Black:{black_count}"f"White:{white_count}")
    def reset(self):
        self.message = ""
        self.visible = False