from games.tic_tac_toe.game import TicTacToeGame
from games.connect4.game import Connect4Game


class GameRegistry:
    _games = {
        "Tic-Tac-Toe": TicTacToeGame,
        "Connect Four": Connect4Game,
    }

    @classmethod
    def get_game_names(cls):
        """
        Returns a list of all registered game names.
        """
        return list(cls._games.keys())

    @classmethod
    def get_game_class(cls, game_name):
        """
        Returns the game class associated with the given name.
        """
        return cls._games.get(game_name)

    @classmethod
    def has_game(cls, game_name):
        """
        Returns True if the specified game is registered.
        """
        return game_name in cls._games

    @classmethod
    def register_game(cls, game_name, game_class):
        """
        Registers a new game.
        """
        cls._games[game_name] = game_class

    @classmethod
    def unregister_game(cls, game_name):
        """
        Removes a game from the registry.
        """
        if game_name in cls._games:
            del cls._games[game_name]

    @classmethod
    def create_game(cls, game_name, renderer):
        """
        Creates and returns a new game instance.
        """
        game_class = cls.get_game_class(game_name)

        if game_class is None:
            raise ValueError(f"Game '{game_name}' is not registered.")

        return game_class(renderer)