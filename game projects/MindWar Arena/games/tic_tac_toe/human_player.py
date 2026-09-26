#games/tic_tac_toe/human_player.py
from engine.core.input import Input
class HumanPlayer:
    def __init__(self, board_renderer):
        self.board_renderer = board_renderer
    def get_action(self, game):
        if game.is_frozen():
            return None
        if not Input.is_left_mouse_clicked():
            return None
        mouse_x, mouse_y = Input.get_mouse_position()
        return self.board_renderer.screen_to_cell(mouse_x,mouse_y,)