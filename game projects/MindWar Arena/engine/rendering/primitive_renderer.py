"""
MindWar Arena

primitive_renderer.py

High-level primitive rendering API.

Responsibilities
----------------
• Draw lines
• Draw rectangles
• Draw circles
• Draw crosses
• Draw grids

Games never interact with ModernGL directly.
"""

from __future__ import annotations

import math

import glm
import moderngl

from engine.rendering.mesh import Mesh
from engine.rendering.shader_manager import ShaderManager
from engine.rendering.camera2d import Camera2D


class PrimitiveRenderer:

    def __init__(
        self,
        context: moderngl.Context,
        camera: Camera2D,
    ):

        self.context = context
        self.camera = camera

        self.shader_manager = ShaderManager(context)

        self.program = self.shader_manager.load_program(
            "primitive",
            "engine/rendering/shaders/primitive.vert",
            "engine/rendering/shaders/primitive.frag",
        )

        self.mesh = Mesh(
            context=self.context,
            program=self.program,
            vertices=[0.0, 0.0],
            dynamic=True,
        )

    # ---------------------------------------------------------
    # Internal
    # ---------------------------------------------------------

    def _set_color(self, color):

        r = color[0] / 255.0
        g = color[1] / 255.0
        b = color[2] / 255.0

        self.program["color"].value = (r, g, b)

    def _set_projection(self):

        projection = self.camera.get_projection()

        self.program["projection"].write(
            projection.to_bytes()
        )

    # ---------------------------------------------------------
    # Frame
    # ---------------------------------------------------------

    def begin_frame(self):

        self._set_projection()

    def end_frame(self):

        pass

    # ---------------------------------------------------------
    # Line
    # ---------------------------------------------------------

    def draw_line(
        self,
        start,
        end,
        color,
    ):

        self._set_color(color)

        vertices = [
            start[0], start[1],
            end[0], end[1],
        ]

        self.mesh.update_vertices(vertices)

        self.mesh.render(moderngl.LINES)

    # ---------------------------------------------------------
    # Rectangle
    # ---------------------------------------------------------

    def draw_rectangle(
        self,
        position,
        size,
        color,
    ):

        x, y = position
        w, h = size

        self.draw_line(
            (x, y),
            (x + w, y),
            color,
        )

        self.draw_line(
            (x + w, y),
            (x + w, y + h),
            color,
        )

        self.draw_line(
            (x + w, y + h),
            (x, y + h),
            color,
        )

        self.draw_line(
            (x, y + h),
            (x, y),
            color,
        )

    # ---------------------------------------------------------
    # Cross
    # ---------------------------------------------------------

    def draw_cross(
        self,
        center,
        size,
        color,
    ):

        half = size / 2

        x = center[0]
        y = center[1]

        self.draw_line(
            (x - half, y - half),
            (x + half, y + half),
            color,
        )

        self.draw_line(
            (x + half, y - half),
            (x - half, y + half),
            color,
        )

    # ---------------------------------------------------------
    # Circle
    # ---------------------------------------------------------

    def draw_circle(
        self,
        center,
        radius,
        color,
        segments=64,
    ):

        self._set_color(color)

        vertices = []

        for i in range(segments + 1):

            angle = (
                i / segments
            ) * math.pi * 2

            x = center[0] + math.cos(angle) * radius
            y = center[1] + math.sin(angle) * radius

            vertices.extend([x, y])

        self.mesh.update_vertices(vertices)

        self.mesh.render(
            moderngl.LINE_STRIP
        )

    # ---------------------------------------------------------
    # Grid
    # ---------------------------------------------------------

    def draw_grid(
        self,
        origin,
        rows,
        columns,
        cell_size,
        color,
    ):

        ox, oy = origin

        width = columns * cell_size
        height = rows * cell_size

        for row in range(rows + 1):

            y = oy + row * cell_size

            self.draw_line(
                (ox, y),
                (ox + width, y),
                color,
            )

        for column in range(columns + 1):

            x = ox + column * cell_size

            self.draw_line(
                (x, oy),
                (x, oy + height),
                color,
            )

    # ---------------------------------------------------------
    # Shutdown
    # ---------------------------------------------------------

    def release(self):

        self.mesh.release()

        self.shader_manager.release()