# engine/rendering/text_texture_cache.py
from __future__ import annotations
from collections import OrderedDict
from typing import Any
import pygame
from engine.rendering.font_manager import FontManager
class TextTextureCache:
    def __init__(self, context: Any, max_size: int = 256) -> None:
        self.context = context
        self.max_size = max_size
        self.cache: OrderedDict[tuple[str, str | None, int, tuple[int, ...]], dict[str, Any]] = (OrderedDict())
    def get_texture(self,text: str,size: int,color: tuple[int, ...],font_name: str | None = None,) -> dict[str, Any]:
        key = (text, font_name, size, tuple(color))
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]
        font = FontManager.get_font(size=size, filename=font_name)
        surface = font.render(text, True, color)
        surface = pygame.transform.flip(surface, False, True)
        texture = self.context.texture(surface.get_size(),4,pygame.image.tostring(surface, "RGBA", True),)
        texture.filter = (self.context.LINEAR, self.context.LINEAR)
        texture.repeat_x = False
        texture.repeat_y = False
        data = {"texture": texture,"width": surface.get_width(),"height": surface.get_height(),}
        if len(self.cache) >= self.max_size:
            _, oldest_data = self.cache.popitem(last=False)
            try:
                oldest_data["texture"].release()
            except Exception:
                pass
        self.cache[key] = data
        return data
    def release(self) -> None:
        for data in self.cache.values():
            try:
                data["texture"].release()
            except Exception:
                pass
        self.cache.clear()