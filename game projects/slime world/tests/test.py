import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Slime World – System Check")

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((20, 20, 30))  # dark background
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
