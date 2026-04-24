from engine.game_loop import GameLoop
from engine.camera import Camera
from world.world import World

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


world = World(width=30, height=20)
camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)


def update(dt):
    world.update(dt)
    camera.follow(world.slime.x, world.slime.y, world.TILE_SIZE)


def render(screen):
    screen.fill((20, 20, 20))
    world.render(screen, camera)


if __name__ == "__main__":
    loop = GameLoop(update, render, SCREEN_WIDTH, SCREEN_HEIGHT)
    loop.run()
