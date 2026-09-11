# games/checkers/overlay_renderer.py
from games.checkers.constants import (GAME_DRAW,GAME_OVER,GAME_RUNNING,PLAYER_BLACK,PLAYER_WHITE,)
class CheckersOverlayRenderer:
    def __init__(self, renderer):
        self.renderer = renderer
    def reset(self):
        pass
    def render(self, game):
        if game is None:
            return
        game_state = game.get_state()
        if game_state is None:
            return
        game_status = game_state.get("game_state",GAME_RUNNING,)
        if game_status == GAME_RUNNING:
            return
        if game_status == GAME_OVER:
            self._render_game_over(game_state)
            return
        if game_status == GAME_DRAW:
            self._render_draw()
    def _render_game_over(self, game_state):
        winner = game_state.get("winner")
        if winner == PLAYER_BLACK:
            message = "Black Wins"
        elif winner == PLAYER_WHITE:
            message = "White Wins"
        else:
            message = "Game Over"
        self._draw_overlay_message(message)
    def _render_draw(self):
        self._draw_overlay_message("Draw")
    def _draw_overlay_message(self, message):
        if hasattr(self.renderer,"draw_overlay_message",):
            self.renderer.draw_overlay_message(message=message,size=56,)
    def _draw_text(self, text, position):
        if hasattr(self.renderer,"draw_text",):
            self.renderer.draw_text(text,position,)
    @staticmethod
    def _get_status_position():
        return 40, 10