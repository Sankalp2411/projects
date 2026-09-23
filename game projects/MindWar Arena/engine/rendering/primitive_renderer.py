# engine/rendering/primitive_renderer.py
import math
from pathlib import Path
import moderngl
from engine.rendering.camera2d import Camera2D
from engine.rendering.mesh import Mesh
from engine.rendering.shader_manager import ShaderManager
_SHADERS_DIR = Path(__file__).resolve().parent / "shaders"
_UNIT_CIRCLE_CACHE: dict[int, list[tuple[float, float]]] = {}
def _get_circle_offsets(segments: int) -> list[tuple[float, float]]:
    if segments not in _UNIT_CIRCLE_CACHE:
        _UNIT_CIRCLE_CACHE[segments] = [(math.cos((i / segments) * math.pi * 2), math.sin((i / segments) * math.pi * 2)) for i in range(segments + 1)]
    return _UNIT_CIRCLE_CACHE[segments]
class PrimitiveRenderer:
    def __init__(self, context: moderngl.Context, camera: Camera2D):
        self.context = context
        self.camera = camera
        self.shader_manager = ShaderManager(context)
        vert_path = str(_SHADERS_DIR / "primitive.vert")
        frag_path = str(_SHADERS_DIR / "primitive.frag")
        self.program = self.shader_manager.load_program("primitive", vert_path, frag_path)
        self.mesh = Mesh(context=self.context,program=self.program,vertices=[0.0, 0.0],dynamic=True,)
    def _set_color(self, color):
        if len(color) == 3:
            r, g, b = color
            a = 255
        else:
            r, g, b, a = color
        self.program["color"].value = (r / 255,g / 255,b / 255,a / 255,)
    def _set_projection(self):
        projection = self.camera.get_projection()
        self.program["projection"].write(projection.to_bytes())
    def begin_frame(self):
        self._set_projection()
    def end_frame(self):
        pass
    def draw_line(self,start,end,color,):
        self._set_color(color)
        vertices = [start[0],start[1],end[0],end[1],]
        self.mesh.update_vertices(vertices)
        self.mesh.render(moderngl.LINES)
    def draw_rectangle(self,position,size,color,):
        x, y = position
        w, h = size
        self.draw_line((x, y),(x + w, y),color,)
        self.draw_line((x + w, y),(x + w, y + h),color,)
        self.draw_line((x + w, y + h),(x, y + h),color,)
        self.draw_line((x, y + h),(x, y),color,)
    def draw_filled_rectangle(self,position,size,color,):
        self._set_color(color)
        x, y = position
        width, height = size
        vertices = [x,y,x + width,y,x,y + height,x,y + height,x + width,y,x + width,y + height,]
        self.mesh.update_vertices(vertices)
        self.mesh.render(moderngl.TRIANGLES)
    def draw_cross(self,center,size,color,):
        half = size / 2
        x = center[0]
        y = center[1]
        self.draw_line((x - half, y - half),(x + half, y + half),color,)
        self.draw_line((x + half, y - half),(x - half, y + half),color,)
    def draw_circle(self, center, radius, color, segments=64):
        self._set_color(color)
        offsets = _get_circle_offsets(segments)
        cx, cy = center
        vertices = []
        for cos_a, sin_a in offsets:
            vertices.extend([cx + cos_a * radius, cy + sin_a * radius])
        self.mesh.update_vertices(vertices)
        self.mesh.render(moderngl.LINE_STRIP)
    def draw_filled_circle(self, center, radius, color, segments=64):
        self._set_color(color)
        offsets = _get_circle_offsets(segments)
        cx, cy = center
        vertices = [cx, cy]
        for cos_a, sin_a in offsets:
            vertices.extend([cx + cos_a * radius, cy + sin_a * radius])
        self.mesh.update_vertices(vertices)
        self.mesh.render(moderngl.TRIANGLE_FAN)
    def draw_grid(self, origin, rows, columns, cell_size, color):
        ox, oy = origin
        width = columns * cell_size
        height = rows * cell_size
        self._set_color(color)
        vertices = []
        for row in range(rows + 1):
            y = oy + row * cell_size
            vertices.extend([ox, y, ox + width, y])
        for column in range(columns + 1):
            x = ox + column * cell_size
            vertices.extend([x, oy, x, oy + height])
        self.mesh.update_vertices(vertices)
        self.mesh.render(moderngl.LINES)
    def release(self):
        self.mesh.release()
        self.shader_manager.release()