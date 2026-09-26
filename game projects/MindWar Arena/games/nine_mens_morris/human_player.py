#games/nine_mens_morris/human_player.py
from engine.core.input import Input
from games.nine_mens_morris.constants import (PHASE_PLACEMENT,PHASE_MOVEMENT,PHASE_FLYING,)
class HumanPlayer:
    def __init__(self, board_renderer):
        self.board_renderer = board_renderer
        self.selected_position = None
    def reset(self):
        self.selected_position = None
    def get_action(self, game):
        if game.is_frozen():
            return None
        if not Input.is_left_mouse_clicked():
            return None
        mouse_x, mouse_y = Input.get_mouse_position()
        position = self.board_renderer.screen_to_position(mouse_x,mouse_y,)
        if position is None:
            return None
        if game.get_phase() == PHASE_PLACEMENT:
            self.selected_position = None
            return position
        if game.is_capture_pending():
            self.selected_position = None
            return position
        if self.selected_position is None:
            if game.get_board().get_position(position) == game.get_current_player():
                self.selected_position = position
            return None
        source = self.selected_position
        self.selected_position = None
        return (source, position)