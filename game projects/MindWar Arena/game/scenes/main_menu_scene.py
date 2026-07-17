#game/scences/main_menu_scene.py
from engine.core.scene import Scene
from engine.utils.logger import Logger
class MainMenuScene(Scene):
    def __init__(self):
        super().__init__("Main Menu")
    def enter(self):
        super().enter()
        Logger.info("[MainMenuScene] Ready")
    def update(self):
        pass
    def render(self):
        pass