#launcher.py
from engine.game_manager import GameManager
class Launcher:
    def __init__(self):
        self.game_manager = GameManager()
    def start(self):
        self.game_manager.initialize()
        self.game_manager.run()
        self.game_manager.shutdown()