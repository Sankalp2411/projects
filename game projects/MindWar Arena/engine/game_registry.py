# engine/game_registry.py
from __future__ import annotations
import importlib
from typing import Any
_GAME_SPECS: dict[str, tuple[str, str]] = {"Tic-Tac-Toe": ("games.tic_tac_toe.game", "TicTacToeGame"),"Connect Four": ("games.connect4.game", "Connect4Game"),"Gomoku": ("games.gomoku.game", "GomokuGame"),"Pente": ("games.pente.game", "PenteGame"),"Othello": ("games.othello.game", "OthelloGame"),"Checkers": ("games.checkers.game", "CheckersGame"),"Chess": ("games.chess.game", "ChessGame"),"Nine Men's Morris": ("games.nine_mens_morris.game", "NineMensMorrisGame"),"Go": ("games.go.game", "GoGame"),}
class GameRegistry:
    _cache: dict[str, type[Any] | None] = {}
    @classmethod
    def get_game_names(cls) -> list[str]:
        return list(_GAME_SPECS.keys())
    @classmethod
    def get_game_class(cls, game_name: str) -> type[Any] | None:
        if game_name in cls._cache:
            return cls._cache[game_name]
        spec = _GAME_SPECS.get(game_name)
        if spec is None:
            return None
        module_path, class_name = spec
        try:
            module = importlib.import_module(module_path)
            game_class = getattr(module, class_name)
            cls._cache[game_name] = game_class
            return game_class
        except (ImportError, AttributeError) as exc:
            from engine.utils.logger import Logger
            Logger.error(f"[GameRegistry] Failed to load '{game_name}': {exc}")
            cls._cache[game_name] = None
            return None
    @classmethod
    def has_game(cls, game_name: str) -> bool:
        return game_name in _GAME_SPECS
    @classmethod
    def register_game(cls, game_name: str, game_class: type[Any]) -> None:
        _GAME_SPECS[game_name] = (game_class.__module__, game_class.__name__)
        cls._cache[game_name] = game_class
    @classmethod
    def unregister_game(cls, game_name: str) -> None:
        _GAME_SPECS.pop(game_name, None)
        cls._cache.pop(game_name, None)
    @classmethod
    def create_game(cls, game_name: str, renderer: Any) -> Any:
        game_class = cls.get_game_class(game_name)
        if game_class is None:
            raise ValueError(f"Game '{game_name}' is not registered.")
        return game_class(renderer)