"""
MindWar Arena

text_renderer.py

High-level text rendering system.

Responsibilities
----------------
• Render cached text textures.
• Manage the text rendering pipeline.
• Use a reusable textured quad.
• Hide all OpenGL details from the engine.

This class NEVER:
• Loads fonts directly.
• Creates text every frame.
• Manages UI layout.
"""

from __future__ import annotations

from engine.rendering.mesh import Mesh
from engine.rendering.shader_manager import ShaderManager
from engine.rendering.text_texture_cache import TextTextureCache


class TextRenderer:

    def __init__(
        self,
        context,
        camera,
    ):

        self.context = context

        self.camera = camera

        # ----------------------------------------
        # Shader Manager
        # ----------------------------------------

        self.shader_manager = ShaderManager(context)

        self.program = self.shader_manager.load_program(
            "text",
            "engine/rendering/shaders/text.vert",
            "engine/rendering/shaders/text.frag",
        )

        # ----------------------------------------
        # Texture Cache
        # ----------------------------------------

        self.cache = TextTextureCache(context)

        # ----------------------------------------
        # Reusable Quad Mesh
        #
        # Vertex Layout:
        #
        # x y u v
        #
        # Six vertices (two triangles)
        # ----------------------------------------

        self.mesh = Mesh(
            context=context,
            program=self.program,
            vertices=[0.0] * 24,
            vertex_format="2f 2f",
            attributes=(
                "in_position",
                "in_uv",
            ),
            dynamic=True,
        )

        self._set_projection()

    # ---------------------------------------------------------
    # Internal
    # ---------------------------------------------------------

    def _set_projection(self):

        projection = self.camera.get_projection()

        self.program["projection"].write(
            projection.to_bytes()
        )
        # ---------------------------------------------------------
    # Quad Builder
    # ---------------------------------------------------------

    def _build_quad(
        self,
        x,
        y,
        width,
        height,
    ):
        """
        Build a textured quad.

        Returns
        -------
        list[float]

        Vertex layout:

            x y u v
        """

        left = x
        right = x + width

        top = y
        bottom = y + height

        return [

            # Triangle 1

            left,  top,    0.0, 0.0,
            right, top,    1.0, 0.0,
            left,  bottom, 0.0, 1.0,

            # Triangle 2

            left,  bottom, 0.0, 1.0,
            right, top,    1.0, 0.0,
            right, bottom, 1.0, 1.0,
        ]
    
        # ---------------------------------------------------------
    # Public
    # ---------------------------------------------------------

    def draw_text(
        self,
        text,
        position,
        size=32,
        color=(255, 255, 255),
        font_name=None,
    ):
        """
        Render text.

        Parameters
        ----------
        text : str

        position : tuple(float, float)

        size : int

        color : tuple

        font_name : str | None
        """

        # ----------------------------------------
        # Retrieve cached texture
        # ----------------------------------------

        cached = self.cache.get_texture(
            text=text,
            font_name=font_name,
            size=size,
            color=color,
        )
        texture = cached["texture"]
        width = cached["width"] 
        height = cached["height"]

        # ----------------------------------------
        # Build quad
        # ----------------------------------------

        vertices = self._build_quad(
            x=position[0],
            y=position[1],
            width=width,
            height=height,
        )

        # ----------------------------------------
        # Upload vertices
        # ----------------------------------------

        self.mesh.update_vertices(vertices)

        # ----------------------------------------
        # Update projection
        # ----------------------------------------

        self._set_projection()
        
        # ----------------------------------------
        # Bind texture
        # ----------------------------------------

        texture.use(location=0)

        self.program["text_texture"].value = 0

        # ----------------------------------------
        # Render
        # ----------------------------------------

        self.mesh.render(
            mode=self.context.TRIANGLES
        )

            # ---------------------------------------------------------
    # Shutdown
    # ---------------------------------------------------------

    def release(self):
        """
        Release all GPU resources owned by the text renderer.
        """

        if self.mesh is not None:
            self.mesh.release()

        if self.cache is not None:
            self.cache.release()

        if self.shader_manager is not None:
            self.shader_manager.release()