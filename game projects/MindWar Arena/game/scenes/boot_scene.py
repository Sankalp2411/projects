"""
MindWar Arena

boot_scene.py

Boot scene responsible for initializing the engine and
transitioning to the first playable scene.
"""

from engine.core.scene import Scene
from engine.utils.logger import Logger

from game.scenes.game_scene import GameScene

from games.tic_tac_toe.game import TicTacToeGame


class BootScene(Scene):
    """
    Initial scene displayed when the engine starts.
    """

    def __init__(self):
        super().__init__("Boot Scene")

    def enter(self):
        """
        Enter the boot scene.
        """

        super().enter()

        Logger.info("[BootScene] Engine initialization complete.")
        Logger.info("[BootScene] Launching Tic-Tac-Toe...")

        game = TicTacToeGame(self.renderer)

        self.scene_manager.change_scene(
            GameScene(game)
        )

    def update(self):
        pass

    def render(self):
        pass