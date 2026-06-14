from engine.interfaces.ai_interface import AIInterface
from engine.utils.logger import Logger
class TestAI(AIInterface):
    def initialize(self):
        Logger.info("[TestAI] Initialized")
    def select_action(self,game_state):
        return None
    def learn(self,state,action,reward,next_state):
        pass
    def reset(self):
        Logger.info("[TestAI] Reset")