"""
MindWar Arena
Phase 2 - Tic-Tac-Toe

constants.py

This module contains every constant used by the Tic-Tac-Toe game.
No game-specific magic numbers or hardcoded strings should appear
outside this file.
"""

# ============================================================
# Game Information
# ============================================================

GAME_NAME = "Tic-Tac-Toe"
GAME_VERSION = "1.0.0"


# ============================================================
# Board Configuration
# ============================================================

BOARD_ROWS = 3
BOARD_COLUMNS = 3
BOARD_SIZE = BOARD_ROWS * BOARD_COLUMNS
BOARD_DIMENSIONS = (BOARD_ROWS, BOARD_COLUMNS)
WIN_LENGTH = 3


# ============================================================
# Cell Values
# ============================================================

EMPTY = 0
PLAYER_X = 1
PLAYER_O = 2


# ============================================================
# Player Configuration
# ============================================================

FIRST_PLAYER = PLAYER_X


# ============================================================
# Game States
# ============================================================

GAME_NOT_STARTED = 0
GAME_RUNNING = 1
GAME_DRAW = 2
GAME_OVER = 3


# ============================================================
# Winner States
# ============================================================

NO_WINNER = 0
X_WINS = PLAYER_X
O_WINS = PLAYER_O


# ============================================================
# Player Types
# ============================================================

HUMAN_PLAYER = 0
AI_PLAYER = 1


# ============================================================
# AI Difficulty Levels
# ============================================================

AI_RANDOM = "Random"
AI_EASY = "Easy"
AI_MEDIUM = "Medium"
AI_HARD = "Hard"


# ============================================================
# Board Rendering
# (Used in later rendering steps)
# ============================================================

CELL_SIZE = 150

BOARD_LINE_WIDTH = 4

SYMBOL_LINE_WIDTH = 8

BOARD_PADDING = 40

X_SYMBOL = "X"
O_SYMBOL = "O"
EMPTY_SYMBOL = "."

# ============================================================
# Colors (RGB)
# (Used later during rendering)
# ============================================================

BACKGROUND_COLOR = (30, 30, 30)

GRID_COLOR = (220, 220, 220)

X_COLOR = (70, 170, 255)

O_COLOR = (255, 120, 120)

WIN_LINE_COLOR = (50, 255, 50)


# ============================================================
# Input
# ============================================================

LEFT_MOUSE_BUTTON = 1


# ============================================================
# Logging Messages
# ============================================================

LOG_GAME_STARTED = "[TicTacToe] Game Started"

LOG_GAME_RESET = "[TicTacToe] Game Reset"

LOG_PLAYER_MOVED = "[TicTacToe] Player Move"

LOG_AI_MOVED = "[TicTacToe] AI Move"

LOG_GAME_OVER = "[TicTacToe] Game Over"


# ============================================================
# Default Game Mode
# ============================================================

GAME_MODE_HUMAN_VS_HUMAN = 0
GAME_MODE_HUMAN_VS_AI = 1
GAME_MODE_AI_VS_AI = 2

DEFAULT_GAME_MODE = GAME_MODE_HUMAN_VS_HUMAN