#games/go/overlay_renderer.py
from games.go.constants import (PLAYER_BLACK,PLAYER_WHITE,)
class GoOverlayRenderer:
    def __init__(self, renderer):
        self.renderer = renderer
    def reset(self):
        pass
    def render(self,result,board,consecutive_passes=0,):
        if result is None:
            return
        if not result.game_over:
            return
        black_score = self._get_score(result,board,PLAYER_BLACK,)
        white_score = self._get_score(result,board,PLAYER_WHITE,)
        if result.draw:
            message = (f"DRAW - "f"BLACK: {black_score:.1f} "f"WHITE: {white_score:.1f}")
        elif result.winner == PLAYER_BLACK:
            message = (f"BLACK WINS - "f"BLACK: {black_score:.1f} "f"WHITE: {white_score:.1f}")
        elif result.winner == PLAYER_WHITE:
            message = (f"WHITE WINS - "f"BLACK: {black_score:.1f} "f"WHITE: {white_score:.1f}")
        else:
            message = "GAME OVER"
        if hasattr(self.renderer,"draw_overlay_message",):
            self.renderer.draw_overlay_message(message)
    @staticmethod
    def _get_score(result,board,player,):
        scores = getattr(result,"scores",None,)
        if isinstance(scores, dict):
            return scores.get(player,0.0,)
        from games.go.rules import GoRules
        return GoRules.calculate_score(board,player,)