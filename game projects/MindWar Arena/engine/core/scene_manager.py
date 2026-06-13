# engine/core/scene_manager.py


class SceneManager:

    def __init__(self):

        self.current_scene = None

    def change_scene(self, scene):

        if self.current_scene:

            self.current_scene.exit()

        self.current_scene = scene

        self.current_scene.enter()

    def update(self):

        if self.current_scene:

            self.current_scene.update()

    def render(self):

        if self.current_scene:

            self.current_scene.render()