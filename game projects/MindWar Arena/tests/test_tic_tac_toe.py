"""
MindWar Arena
Phase 2
Step 6 Rendering Test

Part D
-------
Symbol Rendering

Part E
-------
Rendering Stress Test

Expected Result
---------------
Board:

 X | O | X
-----------
 O | X | O
-----------
 X | . | O

Verify:
- X rendering
- O rendering
- Symbol centering
- Symbol size
- No flickering
- Stable rendering
"""

import pygame

from engine.core.window import Window
from engine.core.renderer import Renderer
from engine.utils.logger import Logger

from games.tic_tac_toe.board import TicTacToeBoard
from games.tic_tac_toe.board_renderer import BoardRenderer

from games.tic_tac_toe.constants import (
    PLAYER_X,
    PLAYER_O,
)

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720


def main():

    Logger.initialize()

    pygame.init()

    window = Window(
        width=WINDOW_WIDTH,
        height=WINDOW_HEIGHT,
        title="Step 6 Test - Symbol Rendering",
    )

    window.create()

    renderer = Renderer()
    renderer.initialize(
        WINDOW_WIDTH,
        WINDOW_HEIGHT,
    )

    board = TicTacToeBoard()

    # ----------------------------------------
    # Test Position
    # ----------------------------------------

    board.set_cell(0, 0, PLAYER_X)
    board.set_cell(0, 1, PLAYER_O)
    board.set_cell(0, 2, PLAYER_X)

    board.set_cell(1, 0, PLAYER_O)
    board.set_cell(1, 1, PLAYER_X)
    board.set_cell(1, 2, PLAYER_O)

    board.set_cell(2, 0, PLAYER_X)
    # (2,1) intentionally left empty
    board.set_cell(2, 2, PLAYER_O)

    board_renderer = BoardRenderer(renderer)

    running = True

    clock = pygame.time.Clock()

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

        renderer.begin_frame()

        board_renderer.render(board)

        renderer.end_frame()

        window.update()

        clock.tick(60)

    renderer.shutdown()

    window.destroy()

    pygame.quit()


if __name__ == "__main__":
    main()