"""
MindWar Arena

overlay_renderer.py

Generic overlay rendering system.

Responsibilities
----------------
• Draw game overlays.
• Display centered messages.
• Display modal UI elements.
• Remain independent of any specific game.

This renderer NEVER:
• Reads game logic.
• Modifies game state.
• Handles input.
"""

from __future__ import annotations
from engine.rendering.font_manager import FontManager

class OverlayRenderer:
    """
    Generic overlay renderer.

    Every game in MindWar Arena will use this renderer
    for end-game messages, pause menus, loading screens,
    confirmation dialogs, and future UI overlays.
    """

    def __init__(self, renderer):

        self.renderer = renderer

    # ---------------------------------------------------------
    # Public
    # ---------------------------------------------------------

    def draw_message(
        self,
        message,
        color=(255, 255, 255),
        size=56,
    ):
        """
        Draw a centered overlay message.

        Currently this simply draws text.

        Later this method will also:
        • Darken the background.
        • Draw animated panels.
        • Draw buttons.
        """

        # Window size comes from the camera.
        width = self.renderer.camera.width
        height = self.renderer.camera.height

        #
        # Temporary approximation.
        #
        # A proper text measurement API will replace this later.
        #

        text_width, text_height = FontManager.measure_text(
            text=message,
            size=size,
        )

        x = (width - text_width) / 2
        y = (height - text_height) / 2

        self.renderer.draw_text(
            text=message,
            position=(x, y),
            size=size,
            color=color,
        )
        # ---------------------------------------------------------
    # Shutdown
    # ---------------------------------------------------------

    def release(self):
        """
        Release overlay resources.

        Reserved for future GPU/UI resources.
        """

        pass