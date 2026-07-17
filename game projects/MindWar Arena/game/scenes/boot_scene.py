#game/scenes/boot_scene.py
from engine.core.scene import Scene
from engine.utils.logger import Logger
from game.scenes.game_scene import GameScene
from games.tic_tac_toe.game import TicTacToeGame
class BootScene(Scene):
    def __init__(self):
        super().__init__("Boot Scene")
    def enter(self):
        super().enter()
        Logger.info("[BootScene] Engine initialization complete.")
        Logger.info("[BootScene] Launching Tic-Tac-Toe...")
        game = TicTacToeGame(self.renderer)
        self.scene_manager.change_scene(GameScene(game))
    def update(self):
        pass
    def render(self):
        pass