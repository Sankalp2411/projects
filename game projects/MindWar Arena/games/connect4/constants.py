GAME_NAME = "Connect Four"
GAME_VERSION = "1.0.0"

# ==========================================================
# Board Configuration
# ==========================================================

BOARD_ROWS = 6
BOARD_COLUMNS = 7

WIN_LENGTH = 4

EMPTY = 0

# ==========================================================
# Players
# ==========================================================

PLAYER_RED = 1
PLAYER_YELLOW = 2

FIRST_PLAYER = PLAYER_RED

# ==========================================================
# Game States
# ==========================================================

GAME_NOT_STARTED = 0
GAME_RUNNING = 1
GAME_DRAW = 2
GAME_OVER = 3

NO_WINNER = 0

# ==========================================================
# AI Difficulty
# ==========================================================

AI_RANDOM = "Random"
AI_EASY = "Easy"
AI_MEDIUM = "Medium"
AI_HARD = "Hard"

# ==========================================================
# Rendering
# ==========================================================

CELL_SIZE = 100

BOARD_PADDING = 40

BOARD_LINE_WIDTH = 4
DISC_RADIUS = CELL_SIZE * 0.38

GRID_COLOR = (220, 220, 220)

PLAYER_RED_COLOR = (230, 70, 70)
PLAYER_YELLOW_COLOR = (255, 215, 0)

WIN_LINE_COLOR = (50, 255, 50)

# ==========================================================
# Game Modes
# ==========================================================

GAME_MODE_HUMAN_VS_HUMAN = 0
GAME_MODE_HUMAN_VS_AI = 1
GAME_MODE_AI_VS_AI = 2

DEFAULT_GAME_MODE = GAME_MODE_HUMAN_VS_HUMAN