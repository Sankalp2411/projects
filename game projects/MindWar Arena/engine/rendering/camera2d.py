#engine/rendering/camera2d.py
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
        half_width = self.width / self.zoom
        half_height = self.height / self.zoom
        self._projection = glm.ortho(0.0,half_width,half_height,0.0,-1.0,1.0,)
    def resize(self, width: int, height: int):
        self.width = width
        self.height = height
        self.update_projection()
    def set_position(self, x: float, y: float):
        self.position = glm.vec2(x, y)
    def move(self, dx: float, dy: float):
        self.position.x += dx
        self.position.y += dy
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