"""
MindWar Arena
Phase 2 - Tic-Tac-Toe

human_player.py

Human player controller.

Responsibilities
----------------
• Read engine mouse input.
• Convert mouse position to a board cell.
• Return the requested move.

This class NEVER:
• Modifies the board.
• Applies moves.
• Switches turns.
• Knows game rules.
"""

from engine.core.input import Input

class HumanPlayer:
    """
    Human-controlled Tic-Tac-Toe player.
    """

    def __init__(self, board_renderer):

        self.board_renderer = board_renderer

    # ---------------------------------------------------------
    # Public
    # ---------------------------------------------------------

    def get_move(self, game_over=False,):
        if game_over:
            return None

        """
        Return the requested move.

        Returns:
            (row, column)
            or
            None
        """

        if not Input.is_left_mouse_clicked():
            return None

        mouse_x, mouse_y = Input.get_mouse_position()

        return self.board_renderer.screen_to_cell(
            mouse_x,
            mouse_y,
        )