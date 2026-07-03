"""
MindWar Arena

renderer.py

High-level rendering manager.

Responsibilities
----------------
• Own the ModernGL context
• Manage the engine camera
• Manage primitive rendering
• Clear the framebuffer
• Begin/end render frames
"""

import moderngl

from engine.rendering.camera2d import Camera2D
from engine.rendering.primitive_renderer import PrimitiveRenderer
from engine.utils.logger import Logger


class Renderer:

    def __init__(self):

        self.ctx = None

        self.camera = None

        self.primitives = None

    # ---------------------------------------------------------
    # Initialization
    # ---------------------------------------------------------

    def initialize(
        self,
        width: int,
        height: int,
    ):

        self.ctx = moderngl.create_context()

        Logger.info(
            f"[Renderer] OpenGL Version: {self.ctx.info['GL_VERSION']}"
        )

        self.camera = Camera2D(width, height)

        self.primitives = PrimitiveRenderer(
            self.ctx,
            self.camera,
        )

        Logger.info(
            "[Renderer] Rendering system initialized."
        )

    # ---------------------------------------------------------
    # Frame
    # ---------------------------------------------------------

    def begin_frame(self):

        self.ctx.clear(
            red=0.08,
            green=0.08,
            blue=0.10,
            alpha=1.0,
        )

        self.primitives.begin_frame()

    def end_frame(self):

        self.primitives.end_frame()

    # ---------------------------------------------------------
    # Primitive API
    # ---------------------------------------------------------

    def draw_line(
        self,
        start,
        end,
        color,
    ):

        self.primitives.draw_line(
            start,
            end,
            color,
        )

    def draw_rectangle(
        self,
        position,
        size,
        color,
    ):

        self.primitives.draw_rectangle(
            position,
            size,
            color,
        )

    def draw_circle(
        self,
        center,
        radius,
        color,
        segments=64,
    ):

        self.primitives.draw_circle(
            center,
            radius,
            color,
            segments,
        )

    def draw_cross(
        self,
        center,
        size,
        color,
    ):

        self.primitives.draw_cross(
            center,
            size,
            color,
        )

    def draw_grid(
        self,
        origin,
        rows,
        columns,
        cell_size,
        color,
    ):

        self.primitives.draw_grid(
            origin,
            rows,
            columns,
            cell_size,
            color,
        )

    # ---------------------------------------------------------
    # Resize
    # ---------------------------------------------------------

    def resize(
        self,
        width,
        height,
    ):

        self.camera.resize(
            width,
            height,
        )

    # ---------------------------------------------------------
    # Shutdown
    # ---------------------------------------------------------

    def shutdown(self):

        if self.primitives is not None:
            self.primitives.release()

        Logger.info(
            "[Renderer] Shutdown"
        )