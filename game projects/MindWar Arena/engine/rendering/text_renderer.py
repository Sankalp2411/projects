#engine/rendering/text_renderer.py
from __future__ import annotations
from engine.rendering.mesh import Mesh
from engine.rendering.shader_manager import ShaderManager
from engine.rendering.text_texture_cache import TextTextureCache
class TextRenderer:
    def __init__(self,context,camera,):
        self.context = context
        self.camera = camera
        self.shader_manager = ShaderManager(context)
        self.program = self.shader_manager.load_program("text","engine/rendering/shaders/text.vert","engine/rendering/shaders/text.frag",)
        self.cache = TextTextureCache(context)
        self.mesh = Mesh(context=context,program=self.program,vertices=[0.0] * 24,vertex_format="2f 2f",attributes=("in_position","in_uv",),dynamic=True,)
        self._set_projection()
    def _set_projection(self):
        projection = self.camera.get_projection()
        self.program["projection"].write(projection.to_bytes())
    def _build_quad(self,x,y,width,height,):
        left = x
        right = x + width
        top = y
        bottom = y + height
        return [left, top, 0.0, 0.0, right, top, 1.0, 0.0, left, bottom, 0.0, 1.0, left, bottom, 0.0, 1.0, right, top, 1.0, 0.0, right, bottom, 1.0, 1.0,]
    def draw_text(self,text,position,size=32,color=(255, 255, 255),font_name=None,):
        cached = self.cache.get_texture(text=text,font_name=font_name,size=size,color=color,)
        texture = cached["texture"]
        width = cached["width"]
        height = cached["height"]
        vertices = self._build_quad(x=position[0],y=position[1],width=width,height=height,)
        self.mesh.update_vertices(vertices)
        self._set_projection()
        texture.use(location=0)
        self.program["text_texture"].value = 0
        self.mesh.render(mode=self.context.TRIANGLES)
    def release(self):
        if self.mesh is not None:
            self.mesh.release()
        if self.cache is not None:
            self.cache.release()
        if self.shader_manager is not None:
            self.shader_manager.release()