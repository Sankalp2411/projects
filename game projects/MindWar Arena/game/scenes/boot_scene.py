# game/scenes/boot_scene.py

from engine.core.scene import Scene
from engine.utils.logger import Logger


class BootScene(Scene):

    def __init__(self):

        super().__init__(
            "Boot Scene"
        )

    def enter(self):

        super().enter()

        Logger.info(
            "[BootScene] Engine startup checks complete"
        )

    def update(self):

        pass

    def render(self):

        pass