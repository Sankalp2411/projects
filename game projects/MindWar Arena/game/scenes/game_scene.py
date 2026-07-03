"""
MindWar Arena

game_scene.py

Universal gameplay scene.

Responsibilities
----------------
• Own the active game.
• Update the active game.
• Render the active game.

Every playable game inside MindWar Arena
runs inside this scene.

Examples
--------
- Tic-Tac-Toe
- Connect Four
- Gomoku
- Pente
- Othello
- Checkers
- Chess
- Go
- Nine Men's Morris
"""

from engine.core.scene import Scene
from engine.interfaces.game_interface import GameInterface
from engine.utils.logger import Logger


class GameScene(Scene):
    """
    Universal gameplay scene.
    """

    def __init__(self, game: GameInterface):
        """
        Parameters
        ----------
        game
            Any class implementing GameInterface.
        """

        super().__init__("Game Scene")

        if not isinstance(game, GameInterface):
            raise TypeError(
                "GameScene requires an object "
                "implementing GameInterface."
            )

        self.game = game

    # ---------------------------------------------------------
    # Scene Lifecycle
    # ---------------------------------------------------------

    def enter(self):
        """
        Enter the scene.
        """

        super().enter()

        Logger.info("[GameScene] Initializing game.")

        self.game.initialize()

    def exit(self):
        """
        Leave the scene.
        """

        Logger.info("[GameScene] Shutting down game.")

        self.game.shutdown()

        super().exit()

    # ---------------------------------------------------------
    # Frame Update
    # ---------------------------------------------------------

    def update(self):
        """
        Update one frame.
        """

        self.game.update()

    # ---------------------------------------------------------
    # Rendering
    # ---------------------------------------------------------

    def render(self):
        """
        Render one frame.
        """

        self.game.render()