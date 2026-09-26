#game/scene/boot_scene.py
from engine.core.scene import Scene
from engine.utils.logger import Logger
from game.scenes.main_menu_scene import MainMenuScene
class BootScene(Scene):
    def __init__(self):
        super().__init__("Boot Scene")
    def enter(self):
        super().enter()
        Logger.info("[BootScene] Engine initialization complete.")
        Logger.info("[BootScene] Opening Main Menu.")
        self.scene_manager.change_scene(MainMenuScene())
    def update(self):
        pass
    def render(self):
        pass