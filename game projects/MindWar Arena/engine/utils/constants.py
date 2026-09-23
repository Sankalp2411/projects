# engine/utils/constants.py
from enum import Enum, IntEnum, auto
class Difficulty(Enum):
    BEGINNER = "beginner"
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    IMPOSSIBLE = "impossible"
class GameState(IntEnum):
    NOT_STARTED = 0
    RUNNING = 1
    DRAW = 2
    OVER = 3
    PAUSED = 4
class GameMode(IntEnum):
    HUMAN_VS_HUMAN = 0
    HUMAN_VS_AI = 1
    AI_VS_AI = 2
PLAYER_ONE: int = 1
PLAYER_TWO: int = 2
EMPTY: int = 0
NO_WINNER: int = 0
class EventType(Enum):
    ON_MOVE_MADE = auto()
    ON_MOVE_UNDONE = auto()
    ON_MOVE_REDONE = auto()
    ON_UNDO = ON_MOVE_UNDONE
    ON_REDO = ON_MOVE_REDONE
    ON_PIECE_CAPTURED = auto()
    ON_PIECES_CAPTURED = auto()
    ON_TURN_CHANGED = auto()
    ON_GAME_OVER = auto()
    ON_GAME_RESET = auto()
    ON_GAME_STARTED = auto()
    ON_CHECK = auto()
    ON_CHECKMATE = auto()
    ON_STALEMATE = auto()
    ON_AI_THINKING_START = auto()
    ON_AI_THINKING_END = auto()
    ON_AI_MOVE_READY = auto()
    ON_CELL_SELECTED = auto()
    ON_CELL_DESELECTED = auto()
    ON_VALID_MOVES_CHANGED = auto()
    ON_ANIMATION_START = auto()
    ON_ANIMATION_END = auto()
    ON_ENGINE_SHUTDOWN = auto()
DEFAULT_ANIMATION_DURATION: float = 0.3
DEFAULT_ARC_HEIGHT: float = 50.0
DEFAULT_SLIDE_SPEED: float = 400.0
DEFAULT_FLIP_DURATION: float = 0.25
DEFAULT_DROP_DURATION: float = 0.4
DEFAULT_FADE_DURATION: float = 0.2
AI_DEFAULT_SEARCH_DEPTH: int = 4
AI_MAX_SEARCH_DEPTH: int = 20
AI_DEFAULT_TIME_LIMIT: float = 5.0
AI_MCTS_DEFAULT_ITERATIONS: int = 1000
AI_MCTS_EXPLORATION_CONSTANT: float = 1.414
DEFAULT_TURN_TIME_LIMIT: float = 30.0
MAX_BOARD_SIZE: int = 19
MAX_MOVE_HISTORY: int = 10000