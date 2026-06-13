# game/scenes/main_menu_scene.py

from engine.core.scene import Scene


class MainMenuScene(Scene):

    def __init__(self):

        super().__init__("Main Menu")

    def enter(self):

        super().enter()

        print("[MainMenuScene] Ready")

    def update(self):

        pass

    def render(self):

        pass