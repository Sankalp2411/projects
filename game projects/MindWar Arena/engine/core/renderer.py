#engine/core/renderer.py
import moderngl
from engine.rendering.text_renderer import TextRenderer
from engine.rendering.camera2d import Camera2D
from engine.rendering.primitive_renderer import PrimitiveRenderer
from engine.utils.logger import Logger
from engine.rendering.overlay_renderer import OverlayRenderer
class Renderer:
    def __init__(self):
        self.ctx = None
        self.camera = None
        self.primitives = None
        self.text = None
        self.overlay = None
    def initialize(self, width: int, height: int, ):
        self.ctx = moderngl.create_context()
        self.ctx.enable(moderngl.BLEND)
        self.ctx.blend_func = (moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA, )
        self.overlay = OverlayRenderer(self)
        Logger.info(f"[Renderer] OpenGL Version: {self.ctx.info['GL_VERSION']}")
        self.camera = Camera2D(width, height)
        self.primitives = PrimitiveRenderer(self.ctx, self.camera, )
        self.text = TextRenderer(self.ctx,self.camera, )
        Logger.info("[Renderer] Rendering system initialized." )
    def begin_frame(self):
        self.ctx.clear(red=0.08,green=0.08,blue=0.10,alpha=1.0, )
        self.primitives.begin_frame()
    def end_frame(self):
        self.primitives.end_frame()
    def draw_line(self,start,end,color, ):
        self.primitives.draw_line(start,end,color, )
    def draw_rectangle(self,position,size,color, ):
        self.primitives.draw_rectangle(position,size,color, )
    def draw_filled_rectangle(self,position,size,color, ):
        self.primitives.draw_filled_rectangle(position,size,color, )
    def draw_circle(self,center,radius,color,segments=64, ):
        self.primitives.draw_circle(center,radius,color,segments, )
    def draw_cross(self,center,size,color, ):
        self.primitives.draw_cross(center,size,color, )
    def draw_grid(self,origin,rows,columns,cell_size,color, ):
        self.primitives.draw_grid(origin,rows,columns,cell_size,color, )
    def draw_text(self,text,position,size=32,color=(255, 255, 255),font_name=None, ):
        self.text.draw_text(text=text,position=position,size=size,color=color,font_name=font_name,)
    def draw_overlay_message(self,message,color=(255, 255, 255),size=56, ):
        self.overlay.draw_message(message=message,color=color,size=size, )
    def resize(self,width,height, ):
        self.camera.resize(width,height, )
    def shutdown(self):
        if self.primitives is not None:
            self.primitives.release()
        if self.text is not None:
            self.text.release()
        if self.overlay is not None:
            self.overlay.release()
        Logger.info("[Renderer] Shutdown")