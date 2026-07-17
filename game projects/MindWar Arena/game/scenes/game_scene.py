#game/scenes/game_scene.py
from engine.core.scene import Scene
from engine.interfaces.game_interface import GameInterface
from engine.utils.logger import Logger
class GameScene(Scene):
    def __init__(self, game: GameInterface):
        super().__init__("Game Scene")
        if not isinstance(game, GameInterface):
            raise TypeError("GameScene requires an object ""implementing GameInterface.")
        self.game = game
    def enter(self):
        super().enter()
        Logger.info("[GameScene] Initializing game.")
        self.game.initialize()
    def exit(self):
        Logger.info("[GameScene] Shutting down game.")
        self.game.shutdown()
        super().exit()
    def update(self):
        self.game.update()
    def render(self):
        self.game.render()