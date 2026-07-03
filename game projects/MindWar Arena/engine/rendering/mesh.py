"""
MindWar Arena

mesh.py

Reusable GPU mesh abstraction.

Responsibilities
----------------
• Create vertex buffers (VBO)
• Create vertex arrays (VAO)
• Upload vertex data
• Render geometry
• Release GPU resources

All engine renderers should use Mesh instead of interacting
directly with ModernGL buffers.
"""

from __future__ import annotations

import numpy as np

from engine.utils.logger import Logger


class Mesh:
    """
    Generic GPU mesh.

    Supports dynamic vertex updates and rendering.
    """

    def __init__(
        self,
        context,
        program,
        vertices,
        vertex_format: str = "2f",
        attributes=("in_position",),
        dynamic: bool = True,
    ):
        self.context = context
        self.program = program

        self.vertex_format = vertex_format
        self.attributes = attributes

        self.dynamic = dynamic

        self.vbo = None
        self.vao = None
        self.buffer_size = 0
        self._create(vertices)

    # ---------------------------------------------------------
    # Creation
    # ---------------------------------------------------------

    def _create(self, vertices):

        data = np.array(vertices, dtype="f4")
        raw_data = data.tobytes()
        self.buffer_size = len(raw_data)
        self.vbo = self.context.buffer(
            raw_data,
            dynamic=self.dynamic
        )

        self.vao = self.context.vertex_array(
            self.program,
            [
                (
                    self.vbo,
                    self.vertex_format,
                    *self.attributes,
                )
            ],
        )

        Logger.info("[Mesh] GPU mesh created.")

    # ---------------------------------------------------------
    # Update
    # ---------------------------------------------------------

    def update_vertices(self, vertices):
        """
        Replace vertex data.

        If the new vertex data is larger than the current GPU buffer,
        recreate the VBO and VAO automatically.
        """

        data = np.array(vertices, dtype="f4")
        raw_data = data.tobytes()

        if len(raw_data) > self.buffer_size:

            self.buffer_size = len(raw_data)

            if self.vao is not None:
                self.vao.release()

            if self.vbo is not None:
                self.vbo.release()

            self.vbo = self.context.buffer(
                raw_data,
                dynamic=self.dynamic,
            )

            self.vao = self.context.vertex_array(
                self.program,
                [
                    (
                        self.vbo,
                        self.vertex_format,
                        *self.attributes,
                    )
                ],
            )

            Logger.debug(
                f"[Mesh] GPU buffer resized to {self.buffer_size} bytes."
            )

        else:

            self.vbo.write(raw_data)
    # ---------------------------------------------------------
    # Rendering
    # ---------------------------------------------------------

    def render(self, mode):
        """
        Render the mesh.

        Example:
            moderngl.LINES
            moderngl.LINE_STRIP
            moderngl.TRIANGLES
            moderngl.TRIANGLE_STRIP
        """

        self.vao.render(mode=mode)

    # ---------------------------------------------------------
    # Release
    # ---------------------------------------------------------

    def release(self):

        try:
            if self.vao is not None:
                self.vao.release()

            if self.vbo is not None:
                self.vbo.release()

            Logger.info("[Mesh] Released.")

        except Exception as exception:
            Logger.warning(
                f"[Mesh] Release failed: {exception}"
            )