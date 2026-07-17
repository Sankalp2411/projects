#engine/core/scene.py
from engine.utils.logger import Logger
class Scene:
    def __init__(self, name):
        self.name = name
        self.game_manager = None
        self.scene_manager = None
        self.window = None
        self.renderer = None
        self.time_manager = None
    def set_game_manager(self, game_manager):
        self.game_manager = game_manager
        self.scene_manager = game_manager.scene_manager
        self.window = game_manager.window
        self.renderer = game_manager.renderer
        self.time_manager = game_manager.time_manager
    def enter(self):
        Logger.info(f"[Scene] Enter: {self.name}")
    def exit(self):
        Logger.info(f"[Scene] Exit: {self.name}")
    def update(self):
        pass
    def render(self):
        pass