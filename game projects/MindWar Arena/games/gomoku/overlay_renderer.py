# games/gomoku/overlay_renderer.py
from games.gomoku.constants import (PLAYER_BLACK, PLAYER_WHITE,)
class OverlayRenderer:
    def __init__(self, renderer):
        self.renderer = renderer
    def render(self, result):
        if result is None:
            return
        if not result.game_over:
            return
        self.draw_background()
        if result.draw:
            self.draw_draw_overlay()
        else:
            self.draw_winner_overlay(result.winner)
    def draw_background(self):
        pass
    def draw_winner_overlay(self, winner):
        if winner == PLAYER_BLACK:
            message = "Black Wins!"
        elif winner == PLAYER_WHITE:
            message = "White Wins!"
        else:
            return
        self.renderer.draw_overlay_message(message=message,color=(255, 255, 255),size=56,)
    def draw_draw_overlay(self):
        self.renderer.draw_overlay_message(message="Draw Game!",color=(255, 255, 255),size=56,)
    def reset(self):
        pass