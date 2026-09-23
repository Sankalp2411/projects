# engine/interfaces/__init__.py
from engine.interfaces.ai_interface import AIInterface
from engine.interfaces.board_interface import BoardInterface
from engine.interfaces.game_interface import GameInterface
from engine.interfaces.game_result import GameResult, TerminationReason
from engine.interfaces.scene_interface import SceneInterface
__all__ = ["GameInterface","AIInterface","BoardInterface","SceneInterface","GameResult","TerminationReason",]