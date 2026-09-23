# engine/rendering/camera2d.py
from __future__ import annotations
import glm
class Camera2D:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.position = glm.vec2(0.0, 0.0)
        self.zoom = 1.0
        self._projection = None
        self.update_projection()
    def update_projection(self):
        w = self.width / self.zoom
        h = self.height / self.zoom
        left = float(self.position.x)
        right = float(self.position.x + w)
        top = float(self.position.y)
        bottom = float(self.position.y + h)
        self._projection = glm.ortho(left, right, bottom, top, -1.0, 1.0)
    def resize(self, width: int, height: int):
        self.width = width
        self.height = height
        self.update_projection()
    def set_position(self, x: float, y: float):
        self.position = glm.vec2(x, y)
        self.update_projection()
    def move(self, dx: float, dy: float):
        self.position.x += dx
        self.position.y += dy
        self.update_projection()
    def set_zoom(self, zoom: float):
        if zoom <= 0:
            return
        self.zoom = zoom
        self.update_projection()
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