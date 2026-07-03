"""
MindWar Arena

scene_manager.py

Manages scene transitions.

Responsibilities
----------------
- Keep track of the active scene.
- Handle scene changes.
- Inject engine context into scenes.
- Forward update and render calls.
"""


class SceneManager:
    """
    Controls scene transitions.
    """

    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.current_scene = None

    # ---------------------------------------------------------
    # Scene Management
    # ---------------------------------------------------------

    def change_scene(self, scene):
        """
        Change to a new scene.
        """

        if self.current_scene is not None:
            self.current_scene.exit()

        self.current_scene = scene

        # Give the scene access to the engine.
        self.current_scene.set_game_manager(self.game_manager)

        self.current_scene.enter()

    # ---------------------------------------------------------
    # Frame Update
    # ---------------------------------------------------------

    def update(self):
        if self.current_scene is not None:
            self.current_scene.update()

    # ---------------------------------------------------------
    # Rendering
    # ---------------------------------------------------------

    def render(self):
        if self.current_scene is not None:
            self.current_scene.render()

    # ---------------------------------------------------------
    # Accessors
    # ---------------------------------------------------------

    def get_current_scene(self):
        """
        Return the active scene.
        """

        return self.current_scene