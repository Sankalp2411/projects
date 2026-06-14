from engine.interfaces.game_interface import (GameInterface)
from engine.utils.logger import Logger
class TestGame(GameInterface):
    def initialize(self):
        Logger.info("[TestGame] Initialized")
    def reset(self):
        Logger.info("[TestGame] Reset")
    def update(self):
        pass
    def render(self):
        pass
    def get_state(self):
        return {}
    def is_game_over(self):
        return False
    def get_winner(self):
        return None