# engine/core/renderer.py

import moderngl


class Renderer:
    """
    Core rendering system.
    """

    def __init__(self):
        self.ctx = None

    def initialize(self):
        self.ctx = moderngl.create_context()

        print("[Renderer] OpenGL Version:")
        print(self.ctx.info["GL_VERSION"])

    def clear(self):
        self.ctx.clear(
            red=0.08,
            green=0.08,
            blue=0.10,
            alpha=1.0
        )

    def shutdown(self):
        print("[Renderer] Shutdown")