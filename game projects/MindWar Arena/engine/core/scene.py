from engine.utils.logger import Logger
class Scene:
    def __init__(self,name):
        self.name = name
    def enter(self):
        Logger.info(f"[Scene] Enter: {self.name}")
    def exit(self):
        Logger.info(f"[Scene] Exit: {self.name}")
    def update(self):
        pass
    def render(self):
        pass