from abc import ABC
from abc import abstractmethod
class AIInterface(ABC):
    @abstractmethod
    def initialize(self):
        pass
    @abstractmethod
    def select_action(self,game_state):
        pass
    @abstractmethod
    def learn(self,state,action,reward,next_state):
        pass
    @abstractmethod
    def reset(self):
        pass