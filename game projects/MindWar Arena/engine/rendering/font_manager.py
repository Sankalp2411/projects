#engine/rendering/font_manager.py
from pathlib import Path
import pygame
class FontManager:
    _fonts = {}
    _initialized = False
    @classmethod
    def initialize(cls):
        if cls._initialized:
            return
        pygame.font.init()
        cls._initialized = True
    @classmethod
    def get_font(cls,size,filename=None,):
        cls.initialize()
        key = (filename, size)
        if key in cls._fonts:
            return cls._fonts[key]
        if filename is None:
            font = pygame.font.Font(None,size,)
        else:
            path = (Path("assets")/ "fonts"/ filename)
            font = pygame.font.Font(str(path),size,)
        cls._fonts[key] = font
        return font
    @classmethod
    def shutdown(cls):
        cls._fonts.clear()
        pygame.font.quit()
        cls._initialized = False
    @classmethod
    def measure_text(cls,text,size,filename=None,):
        font = cls.get_font(size=size,filename=filename,)
        return font.size(text)