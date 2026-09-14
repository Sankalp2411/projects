# games/chess/overlay_renderer.py
from games.chess.constants import (PLAYER_BLACK,PLAYER_WHITE,)
class ChessOverlayRenderer:
    def __init__(self, renderer):
        self.renderer = renderer
    def reset(self):
        pass
    def render(self,game_state,winner=None,draw=False,):
        if draw:
            self.draw_draw()
            return
        if game_state == "CHECKMATE":
            self.draw_checkmate(winner)
            return
        if game_state == "STALEMATE":
            self.draw_stalemate()
            return
        if game_state == "CHECK":
            self.draw_check()
    def draw_game_over(self,winner=None,draw=False,):
        if draw:
            self.draw_draw()
            return
        if winner is not None:
            self._draw_message(f"{self._get_player_name(winner)} WINS")
            return
        self._draw_message("GAME OVER")
    def draw_checkmate(self,winner=None,):
        if winner is None:
            self._draw_message("CHECKMATE")
            return
        self._draw_message(f"CHECKMATE - "f"{self._get_player_name(winner)} WINS")
    def draw_stalemate(self):
        self._draw_message("STALEMATE - DRAW")
    def draw_check(self):
        self._draw_message("CHECK")
    def draw_draw(self):
        self._draw_message("DRAW")
    @staticmethod
    def _get_player_name(player):
        if player == PLAYER_WHITE:
            return "WHITE"
        if player == PLAYER_BLACK:
            return "BLACK"
        return f"PLAYER {player}"
    def _draw_message(self,message,):
        if hasattr(self.renderer,"draw_overlay_message",):
            self.renderer.draw_overlay_message(message)
            return
        if hasattr(self.renderer,"draw_text",):
            self.renderer.draw_text(message,(40, 20),)