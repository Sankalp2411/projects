import pygame


class Slime:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.color = (200, 50, 200)
        self.speed = 1  # tiles per move
        self.width = 32
        self.height = 32

    def update(self, dt, world):
        # Import World only for type hints (optional)
        # from world.world import World  # REMOVE this top import

        keys = pygame.key.get_pressed()
        nx, ny = self.x, self.y

        if keys[pygame.K_w]:
            ny -= 1
        elif keys[pygame.K_s]:
            ny += 1
        elif keys[pygame.K_a]:
            nx -= 1
        elif keys[pygame.K_d]:
            nx += 1

        if world.is_valid_position(nx, ny):
            current_zone = world.get_zone(self.x, self.y)
            next_zone = world.get_zone(nx, ny)
            if next_zone and next_zone.is_walkable():
                # Check slope
                slope = abs(next_zone.elevation - current_zone.elevation)
                if slope <= 1:
                    self.x, self.y = nx, ny

    def render(self, surface, camera, tile_size: int):
        screen_x, screen_y = camera.apply(
            self.x * tile_size, self.y * tile_size
        )

        pygame.draw.ellipse(
            surface,
            self.color,
            (screen_x + tile_size//4, screen_y + tile_size//4, self.width, self.height)
        )
