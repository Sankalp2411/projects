from engine.core.scene import Scene
from engine.utils.logger import Logger
from engine.utils.asset_manager import AssetManager
from engine.utils.config import Config
class BootScene(Scene):
    def __init__(self):
        super().__init__("Boot Scene")
    def enter(self):
        super().enter()
        Logger.info("[BootScene] Starting Integration Tests")
    def update(self):
        pass
    def render(self):
        pass