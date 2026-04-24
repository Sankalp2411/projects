import pygame


class GameClock:
    def __init__(self, fps: int):
        self.clock = pygame.time.Clock()
        self.fps = fps

    def tick(self) -> float:
        return self.clock.tick(self.fps) / 1000.0
