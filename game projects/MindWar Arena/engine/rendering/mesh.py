#engine/rendering/mesh.py
from __future__ import annotations
import numpy as np
from engine.utils.logger import Logger
class Mesh:
    def __init__(self,context,program,vertices,vertex_format: str = "2f",attributes=("in_position",),dynamic: bool = True, ):
        self.context = context
        self.program = program
        self.vertex_format = vertex_format
        self.attributes = attributes
        self.dynamic = dynamic
        self.vbo = None
        self.vao = None
        self.buffer_size = 0
        self.vertex_count = 0
        self._create(vertices)
    def _create(self, vertices):
        data = np.array(vertices, dtype="f4")
        raw_data = data.tobytes()
        self.buffer_size = len(raw_data)
        self.vbo = self.context.buffer(raw_data,dynamic=self.dynamic)
        self._create_vertex_array()
        Logger.info("[Mesh] GPU mesh created.")
    def _create_vertex_array(self):
        self.vao = self.context.vertex_array(self.program,[(self.vbo,self.vertex_format,*self.attributes, )], )
        return self.vao
    def update_vertices(self, vertices):
        data = np.array(vertices, dtype="f4")
        raw_data = data.tobytes()
        self.vertex_count = len(vertices) // 2
        if len(raw_data) > self.buffer_size:
            self.buffer_size = len(raw_data)
            if self.vao is not None:
                self.vao.release()
            if self.vbo is not None:
                self.vbo.release()
            self.vbo = self.context.buffer(raw_data,dynamic=self.dynamic, )
            self._create_vertex_array()
            Logger.debug(f"[Mesh] GPU buffer resized to {self.buffer_size} bytes.")
        else:
            self.vbo.write(raw_data)
    def rebuild(self, program):
        self.program = program
        if self.vao is not None:
            self.vao.release()
        self._create_vertex_array()
    def render(self, mode):
        self.vao.render(mode=mode,vertices=self.vertex_count, )
    def release(self):
        try:
            if self.vao is not None:
                self.vao.release()
                self.vao = None
            if self.vbo is not None:
                self.vbo.release()
                self.vbo = None
            Logger.info("[Mesh] Released.")
        except Exception as exception:
            Logger.warning(f"[Mesh] Release failed: {exception}")