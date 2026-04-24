# engine/renderer.py

import pygame


class Renderer:
    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self.draw_queue = []

    def draw_rect(self, color, rect, z=0):
        self.draw_queue.append((z, lambda: pygame.draw.rect(self.surface, color, rect)))

    def draw_circle(self, color, position, radius, z=0):
        self.draw_queue.append(
            (z, lambda: pygame.draw.circle(self.surface, color, position, radius))
        )

    def flush(self):
        self.draw_queue.sort(key=lambda item: item[0])
        for _, draw_call in self.draw_queue:
            draw_call()
        self.draw_queue.clear()
