"""
MindWar Arena

tests/test_overlay_renderer.py

Tests the complete overlay rendering system.

Verifies:
• Background overlay
• Text rendering
• Different winner messages
• Draw message
• Renderer shutdown
"""

import pygame

from engine.utils.logger import Logger
from engine.core.window import Window
from engine.core.renderer import Renderer
from engine.core.input import Input


WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720


def main():

    Logger.initialize()

    window = Window(
        WINDOW_WIDTH,
        WINDOW_HEIGHT,
        "Overlay Renderer Test",
    )

    window.create()

    renderer = Renderer()
    renderer.initialize(
        WINDOW_WIDTH,
        WINDOW_HEIGHT,
    )

    Input.initialize()

    running = True

    stage = 0

    stage_duration = 180          # 3 seconds @ 60 FPS
    frame_counter = 0

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

        Input.update()

        renderer.begin_frame()

        # -------------------------------------------------
        # Dummy board behind the overlay
        # -------------------------------------------------

        renderer.draw_grid(
            origin=(200, 120),
            rows=3,
            columns=3,
            cell_size=150,
            color=(180, 180, 180),
        )

        renderer.draw_cross(
            center=(275,195),
            size=70,
            color=(255,80,80),
        )

        renderer.draw_circle(
            center=(425,345),
            radius=35,
            color=(80,180,255),
        )

        # -------------------------------------------------
        # Overlay Messages
        # -------------------------------------------------

        if stage == 0:

            renderer.draw_overlay_message(
                "PLAYER X WINS!",
                color=(255,80,80),
                size=60,
            )

        elif stage == 1:

            renderer.draw_overlay_message(
                "PLAYER O WINS!",
                color=(80,180,255),
                size=60,
            )

        elif stage == 2:

            renderer.draw_overlay_message(
                "DRAW GAME",
                color=(255,255,100),
                size=60,
            )

        elif stage == 3:

            renderer.draw_overlay_message(
                "MindWar Arena",
                color=(255,255,255),
                size=64,
            )

        renderer.end_frame()

        window.update()
        window.tick(60)

        frame_counter += 1

        if frame_counter >= stage_duration:

            frame_counter = 0
            stage += 1

            if stage > 3:
                running = False

    renderer.shutdown()
    window.destroy()


if __name__ == "__main__":
    main()