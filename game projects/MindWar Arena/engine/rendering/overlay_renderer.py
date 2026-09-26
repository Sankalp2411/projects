#engine/rendering/overlay_renderer.py
from __future__ import annotations
from engine.rendering.font_manager import FontManager
class OverlayRenderer:
    def __init__(self, renderer):
        self.renderer = renderer
    def draw_message(self,message,color=(255, 255, 255),size=56,):
        width = self.renderer.camera.width
        height = self.renderer.camera.height
        text_width, text_height = FontManager.measure_text(text=message,size=size,)
        x = (width - text_width) / 2
        y = (height - text_height) / 2
        self.renderer.draw_text(text=message,position=(x, y),size=size,color=color,)
    def release(self):
        pass