"""
MindWar Arena

render_batch.py

Provides a generic render batching interface for the rendering engine.

Current Responsibilities
------------------------
• Store render commands
• Maintain drawing order
• Execute queued draw operations

Future Responsibilities
-----------------------
• Batch identical primitives
• Batch textured rendering
• Reduce GPU draw calls
• Layer-based rendering
• Instanced rendering
• Render sorting

This implementation is intentionally lightweight.
It provides the architecture required for future
optimization without adding unnecessary complexity.
"""


class RenderCommand:
    """
    Represents one render command.
    """

    def __init__(self, function, *args, **kwargs):
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def execute(self):
        self.function(*self.args, **self.kwargs)


class RenderBatch:
    """
    Generic render command queue.
    """

    def __init__(self):
        self._commands = []

    # ---------------------------------------------------------
    # Queue
    # ---------------------------------------------------------

    def add(self, function, *args, **kwargs):
        """
        Queue a render command.
        """

        self._commands.append(
            RenderCommand(
                function,
                *args,
                **kwargs,
            )
        )

    # ---------------------------------------------------------
    # Execute
    # ---------------------------------------------------------

    def render(self):
        """
        Execute all queued commands
        in submission order.
        """

        for command in self._commands:
            command.execute()

    # ---------------------------------------------------------
    # Utility
    # ---------------------------------------------------------

    def clear(self):
        """
        Remove all queued commands.
        """

        self._commands.clear()

    def size(self):
        """
        Number of queued commands.
        """

        return len(self._commands)

    def empty(self):
        """
        True if no commands are queued.
        """

        return len(self._commands) == 0