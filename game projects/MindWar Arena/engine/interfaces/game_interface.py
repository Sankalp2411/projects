#engine/interfaces/game_interface.py
from abc import ABC
from abc import abstractmethod
class GameInterface(ABC):
    @abstractmethod
    def initialize(self):
        pass
    @abstractmethod
    def reset(self):
        pass
    @abstractmethod
    def shutdown(self):
        pass
    @abstractmethod
    def update(self):
        pass
    @abstractmethod
    def render(self):
        pass
    @abstractmethod
    def get_state(self):
        pass
    @abstractmethod
    def get_board(self):
        pass
    @abstractmethod
    def get_current_player(self):
        pass
    @abstractmethod
    def get_winner(self):
        pass
    @abstractmethod
    def is_game_over(self):
        pass
    @abstractmethod
    def make_move(self, *args, **kwargs):
        pass