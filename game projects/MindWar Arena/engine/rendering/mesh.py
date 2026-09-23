# engine/rendering/mesh.py
from __future__ import annotations
import array
from collections.abc import Sequence
from typing import Any
import numpy as np
from engine.utils.logger import Logger
DEFAULT_DYNAMIC_BUFFER_CAPACITY = 65536
class Mesh:
    def __init__(self,context: Any,program: Any,vertices: Sequence[float] | bytes | bytearray,vertex_format: str = "2f",attributes: Sequence[str] = ("in_position",),dynamic: bool = True,):
        self.context = context
        self.program = program
        self.vertex_format = vertex_format
        self.attributes = attributes
        self.dynamic = dynamic
        self.vbo = None
        self.vao = None
        self.buffer_size = 0
        self.components_per_vertex = self._calculate_components(vertex_format)
        self.vertex_count = 0
        self._create(vertices)
    @staticmethod
    def _calculate_components(vertex_format: str) -> int:
        total = 0
        for token in vertex_format.split():
            num = ""
            for ch in token:
                if ch.isdigit():
                    num += ch
                else:
                    break
            total += int(num) if num else 1
        return max(1, total)
    def _to_raw_bytes(self, vertices: Sequence[float] | bytes | bytearray) -> tuple[bytes, int]:
        if isinstance(vertices, (bytes, bytearray, memoryview)):
            raw = bytes(vertices)
            count = len(raw) // (4 * self.components_per_vertex)
            return raw, count
        try:
            arr = array.array("f", vertices)
            raw = arr.tobytes()
            count = len(arr) // self.components_per_vertex
            return raw, count
        except (TypeError, ValueError):
            arr = np.array(vertices, dtype="f4")
            raw = arr.tobytes()
            count = len(vertices) // self.components_per_vertex
            return raw, count
    def _create(self, vertices: Sequence[float] | bytes | bytearray):
        raw_data, count = self._to_raw_bytes(vertices)
        self.vertex_count = count
        if self.dynamic:
            self.buffer_size = max(len(raw_data), DEFAULT_DYNAMIC_BUFFER_CAPACITY)
        else:
            self.buffer_size = len(raw_data)
        try:
            self.vbo = self.context.buffer(reserve=self.buffer_size, dynamic=self.dynamic)
            if raw_data:
                self.vbo.write(raw_data)
        except TypeError:
            self.vbo = self.context.buffer(raw_data, dynamic=self.dynamic)
            self.buffer_size = len(raw_data)
        self._create_vertex_array()
        Logger.info("[Mesh] GPU mesh created.")
    def _create_vertex_array(self):
        if (self.program is not None and self.context is not None and hasattr(self.context, "vertex_array")):
            self.vao = self.context.vertex_array(self.program,[(self.vbo, self.vertex_format, *self.attributes)],)
        return self.vao
    def update_vertices(self, vertices: Sequence[float] | bytes | bytearray):
        raw_data, count = self._to_raw_bytes(vertices)
        self.vertex_count = count
        if len(raw_data) > self.buffer_size:
            self.buffer_size = max(len(raw_data) * 2, DEFAULT_DYNAMIC_BUFFER_CAPACITY)
            if self.vao is not None:
                self.vao.release()
            if self.vbo is not None:
                self.vbo.release()
            try:
                self.vbo = self.context.buffer(reserve=self.buffer_size, dynamic=self.dynamic)
                self.vbo.write(raw_data)
            except TypeError:
                self.vbo = self.context.buffer(raw_data, dynamic=self.dynamic)
                self.buffer_size = len(raw_data)
            self._create_vertex_array()
            Logger.debug(f"[Mesh] GPU buffer resized to {self.buffer_size} bytes.")
        else:
            self.vbo.write(raw_data)
    def rebuild(self, program: Any):
        self.program = program
        if self.vao is not None:
            self.vao.release()
        self._create_vertex_array()
    def render(self, mode: Any):
        if self.vao is not None and self.vertex_count > 0:
            self.vao.render(mode=mode, vertices=self.vertex_count)
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