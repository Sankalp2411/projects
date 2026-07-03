"""
MindWar Arena

scene.py

Base class for every scene in the engine.

A Scene represents one application state such as:
- Boot
- Main Menu
- Gameplay
- Settings
- Pause
- Game Over

The SceneManager injects the GameManager into each scene,
providing convenient access to shared engine systems.
"""

from engine.utils.logger import Logger


class Scene:
    """
    Base class for all engine scenes.
    """

    def __init__(self, name):
        self.name = name

        # Engine context (assigned by SceneManager)
        self.game_manager = None
        self.scene_manager = None
        self.window = None
        self.renderer = None
        self.time_manager = None

    # ---------------------------------------------------------
    # Engine Context
    # ---------------------------------------------------------

    def set_game_manager(self, game_manager):
        """
        Inject the engine context into this scene.

        Called automatically by SceneManager before enter().
        """

        self.game_manager = game_manager
        self.scene_manager = game_manager.scene_manager
        self.window = game_manager.window
        self.renderer = game_manager.renderer
        self.time_manager = game_manager.time_manager

    # ---------------------------------------------------------
    # Scene Lifecycle
    # ---------------------------------------------------------

    def enter(self):
        Logger.info(f"[Scene] Enter: {self.name}")

    def exit(self):
        Logger.info(f"[Scene] Exit: {self.name}")

    def update(self):
        pass

    def render(self):
        pass