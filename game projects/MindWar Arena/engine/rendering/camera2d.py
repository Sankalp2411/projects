"""
MindWar Arena

camera2d.py

Provides a reusable orthographic 2D camera for the rendering engine.

Responsibilities
----------------
• Manage screen dimensions
• Build orthographic projection matrix
• Support future zooming
• Support future camera movement
• Provide screen information to the renderer

This class is completely independent of any specific game.
"""

import glm


class Camera2D:
    """
    Universal 2D camera.

    World Coordinate System

        (0,0) --------------------> +X
          |
          |
          |
          |
          V
         +Y

    Default origin is the upper-left corner,
    matching traditional 2D board games.
    """

    def __init__(self, width: int, height: int):

        self.width = width
        self.height = height

        # Future camera movement
        self.position = glm.vec2(0.0, 0.0)

        # Future zoom
        self.zoom = 1.0

        self._projection = None

        self.update_projection()

    # ---------------------------------------------------------
    # Projection
    # ---------------------------------------------------------

    def update_projection(self):
        """
        Rebuild the orthographic projection matrix.
        """

        half_width = self.width / self.zoom
        half_height = self.height / self.zoom

        self._projection = glm.ortho(
            0.0,
            half_width,
            half_height,
            0.0,
            -1.0,
            1.0,
        )

    # ---------------------------------------------------------
    # Resize
    # ---------------------------------------------------------

    def resize(self, width: int, height: int):
        """
        Update camera after window resize.
        """

        self.width = width
        self.height = height

        self.update_projection()

    # ---------------------------------------------------------
    # Camera Position
    # ---------------------------------------------------------

    def set_position(self, x: float, y: float):

        self.position = glm.vec2(x, y)

    def move(self, dx: float, dy: float):

        self.position.x += dx
        self.position.y += dy

    # ---------------------------------------------------------
    # Zoom
    # ---------------------------------------------------------

    def set_zoom(self, zoom: float):

        if zoom <= 0:
            return

        self.zoom = zoom

        self.update_projection()

    # ---------------------------------------------------------
    # Getters
    # ---------------------------------------------------------

    def get_projection(self):

        return self._projection

    def get_width(self):

        return self.width

    def get_height(self):

        return self.height

    def get_zoom(self):

        return self.zoom

    def get_position(self):

        return self.position