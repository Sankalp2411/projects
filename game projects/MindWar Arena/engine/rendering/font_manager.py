"""
MindWar Arena

font_manager.py

Centralized font loading and caching.

Responsibilities
----------------
• Initialize pygame font subsystem.
• Load fonts.
• Cache loaded fonts.
• Return reusable font objects.

This class NEVER:
• Renders text.
• Draws to the screen.
"""

from pathlib import Path

import pygame


class FontManager:

    _fonts = {}

    _initialized = False

    # ---------------------------------------------------------
    # Initialization
    # ---------------------------------------------------------

    @classmethod
    def initialize(cls):

        if cls._initialized:
            return

        pygame.font.init()

        cls._initialized = True

    # ---------------------------------------------------------
    # Font Loading
    # ---------------------------------------------------------

    @classmethod
    def get_font(
        cls,
        size,
        filename=None,
    ):
        """
        Return a cached font.

        Parameters
        ----------
        size : int

        filename : str | None

            None -> pygame default font
        """

        cls.initialize()

        key = (filename, size)

        if key in cls._fonts:
            return cls._fonts[key]

        if filename is None:

            font = pygame.font.Font(
                None,
                size,
            )

        else:

            path = (
                Path("assets")
                / "fonts"
                / filename
            )

            font = pygame.font.Font(
                str(path),
                size,
            )

        cls._fonts[key] = font

        return font

    # ---------------------------------------------------------
    # Shutdown
    # ---------------------------------------------------------

    @classmethod
    def shutdown(cls):

        cls._fonts.clear()

        pygame.font.quit()

        cls._initialized = False
    
    @classmethod
    def measure_text(
        cls,
        text,
        size,
        filename=None,
    ):
        """
        Measure the rendered size of a text string.

        Returns
        -------
        (width, height)
        """

        font = cls.get_font(
            size=size,
            filename=filename,
        )

        return font.size(text)