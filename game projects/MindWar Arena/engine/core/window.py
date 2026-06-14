import pygame
from engine.utils.logger import Logger
class Window:
    def __init__(self,width,height,title):
        self.width = width
        self.height = height
        self.title = title
        self.screen = None
        self.clock = None
    def create(self):
        pygame.init()
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION,3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION,3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK,pygame.GL_CONTEXT_PROFILE_CORE)
        self.screen = pygame.display.set_mode((self.width, self.height),pygame.OPENGL | pygame.DOUBLEBUF)
        pygame.display.set_caption(self.title)
        self.clock = pygame.time.Clock()
        Logger.info(f"[Window] Created "f"{self.width}x{self.height}")
    def update(self):
        pygame.display.flip()
    def tick(self,fps=60):
        self.clock.tick(fps)
    def destroy(self):
        pygame.quit()
        Logger.info("[Window] Destroyed")