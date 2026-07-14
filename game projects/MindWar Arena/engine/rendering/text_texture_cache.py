"""
MindWar Arena

text_texture_cache.py

Caches rendered text as OpenGL textures.

Responsibilities
----------------
• Render text to pygame surfaces.
• Convert surfaces to OpenGL textures.
• Cache textures.
• Reuse cached textures.
• Release textures during shutdown.

This class NEVER:
• Draws text.
• Chooses positions.
• Performs alignment.
"""

import pygame

from engine.rendering.font_manager import FontManager


class TextTextureCache:

    def __init__(self, context):

        self.context = context

        self.cache = {}

    # ---------------------------------------------------------
    # Public
    # ---------------------------------------------------------

    def get_texture(
        self,
        text,
        size,
        color,
        font_name=None,
    ):
        """
        Return a cached OpenGL texture for the requested text.

        Returns
        -------
        dict

            {
                "texture": Texture,
                "width": int,
                "height": int,
            }
        """

        key = (
            text,
            font_name,
            size,
            color,
        )

        if key in self.cache:
            return self.cache[key]

        font = FontManager.get_font(
            size=size,
            filename=font_name,
        )

        surface = font.render(
            text,
            True,
            color,
        )

        surface = pygame.transform.flip(
            surface,
            False,
            True,
        )

        texture = self.context.texture(
            surface.get_size(),
            4,
            pygame.image.tostring(
                surface,
                "RGBA",
                True,
            ),
        )

        texture.filter = (
            self.context.LINEAR,
            self.context.LINEAR,
        )

        texture.repeat_x = False
        texture.repeat_y = False

        data = {
            "texture": texture,
            "width": surface.get_width(),
            "height": surface.get_height(),
        }

        self.cache[key] = data

        return data

    # ---------------------------------------------------------
    # Shutdown
    # ---------------------------------------------------------

    def release(self):

        for data in self.cache.values():

            data["texture"].release()

        self.cache.clear()