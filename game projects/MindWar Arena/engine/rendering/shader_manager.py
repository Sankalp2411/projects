"""
MindWar Arena

shader_manager.py

Centralized GLSL shader management.

Responsibilities
----------------
• Load shader source files
• Compile shader programs
• Cache compiled programs
• Retrieve shader programs
• Release GPU resources

All engine systems should obtain shader programs through this
manager rather than interacting with ModernGL directly.
"""

from pathlib import Path

from engine.utils.logger import Logger


class ShaderManager:

    def __init__(self, context):

        self.context = context
        self._programs = {}

    # ---------------------------------------------------------
    # Internal
    # ---------------------------------------------------------

    @staticmethod
    def _read_shader(path: str) -> str:
        """
        Read a GLSL shader source file.
        """

        shader_path = Path(path)

        if not shader_path.exists():
            raise FileNotFoundError(
                f"Shader file not found: {shader_path}"
            )

        return shader_path.read_text(encoding="utf-8")

    # ---------------------------------------------------------
    # Program Loading
    # ---------------------------------------------------------

    def load_program(
        self,
        name: str,
        vertex_shader_path: str,
        fragment_shader_path: str,
    ):
        """
        Load and compile a shader program.

        If the program already exists, the cached version
        is returned.
        """

        if name in self._programs:
            Logger.warning(
                f"[ShaderManager] Shader '{name}' already loaded."
            )
            return self._programs[name]

        vertex_source = self._read_shader(vertex_shader_path)
        fragment_source = self._read_shader(fragment_shader_path)

        program = self.context.program(
            vertex_shader=vertex_source,
            fragment_shader=fragment_source,
        )

        self._programs[name] = program

        Logger.info(
            f"[ShaderManager] Loaded shader '{name}'."
        )

        return program

    # ---------------------------------------------------------
    # Access
    # ---------------------------------------------------------

    def get_program(self, name: str):

        return self._programs.get(name)

    def has_program(self, name: str):

        return name in self._programs

    # ---------------------------------------------------------
    # Shutdown
    # ---------------------------------------------------------

    def release(self):

        for name, program in self._programs.items():

            try:
                program.release()

                Logger.info(
                    f"[ShaderManager] Released '{name}'."
                )

            except Exception as exception:

                Logger.warning(
                    f"[ShaderManager] Failed to release '{name}': {exception}"
                )

        self._programs.clear()