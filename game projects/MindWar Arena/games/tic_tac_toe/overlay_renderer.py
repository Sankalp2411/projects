"""
MindWar Arena
Phase 2 - Tic-Tac-Toe

overlay_renderer.py

Responsible for rendering end-of-game overlays.

Responsibilities
----------------
• Winner overlay
• Draw overlay
• Future restart UI
• Future menu UI

This renderer NEVER:
• Modifies the game
• Reads input
• Changes turns
• Draws the board
"""

from games.tic_tac_toe.constants import (
    PLAYER_X,
    PLAYER_O,
)


class OverlayRenderer:
    """
    Renders end-of-game overlays.
    """

    def __init__(self, renderer):

        self.renderer = renderer

    # ---------------------------------------------------------
    # Public
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # Background
    # ---------------------------------------------------------

    def draw_background(self):
        """
        Placeholder.

        Future:
            Semi-transparent dark overlay.
        """

        pass

    # ---------------------------------------------------------
    # Winner
    # ---------------------------------------------------------

    def draw_winner_overlay(self, winner):

        if winner == PLAYER_X:
            message = "Player X Wins!"
        elif winner == PLAYER_O:
            message = "Player O Wins!"
        else:
            return

        self.renderer.draw_overlay_message(
            message=message,
            color=(255,255,255),
            size=56,
        )

    # ---------------------------------------------------------
    # Draw
    # ---------------------------------------------------------

    def draw_draw_overlay(self):

        self.renderer.draw_overlay_message(
            message="Draw Game!",
            color=(255,255,255),
            size=56,
        )
    
    def reset(self):
        """
        Reset overlay visual state.

        Future:
            • fade animations
            • popup animation
            • restart menu
            • transitions
        """

        pass