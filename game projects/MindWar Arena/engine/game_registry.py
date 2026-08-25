#engine/game_registry.py
from games.tic_tac_toe.game import TicTacToeGame
from games.connect4.game import Connect4Game
from games.gomoku.game import GomokuGame
class GameRegistry:
    _games = {"Tic-Tac-Toe": TicTacToeGame,"Connect Four": Connect4Game,"Gomoku": GomokuGame,}
    @classmethod
    def get_game_names(cls):
        return list(cls._games.keys())
    @classmethod
    def get_game_class(cls, game_name):
        return cls._games.get(game_name)
    @classmethod
    def has_game(cls, game_name):
        return game_name in cls._games
    @classmethod
    def register_game(cls, game_name, game_class):
        cls._games[game_name] = game_class
    @classmethod
    def unregister_game(cls, game_name):
        if game_name in cls._games:
            del cls._games[game_name]
    @classmethod
    def create_game(cls, game_name, renderer):
        game_class = cls.get_game_class(game_name)
        if game_class is None:
            raise ValueError(f"Game '{game_name}' is not registered.")
        return game_class(renderer)