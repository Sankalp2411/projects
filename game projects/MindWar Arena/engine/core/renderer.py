# engine/core/renderer.py

import moderngl

from engine.utils.logger import Logger


class Renderer:

    def __init__(self):

        self.ctx = None

    def initialize(self):

        self.ctx = moderngl.create_context()

        Logger.info(
            "[Renderer] OpenGL Version:"
        )

        Logger.info(
            self.ctx.info["GL_VERSION"]
        )

    def clear(self):

        self.ctx.clear(
            red=0.08,
            green=0.08,
            blue=0.10,
            alpha=1.0
        )

    def shutdown(self):

        Logger.info(
            "[Renderer] Shutdown"
        )