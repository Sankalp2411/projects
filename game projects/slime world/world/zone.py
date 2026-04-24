import pygame
from world.terrain import TerrainType


class Zone:
    def __init__(self, x: int, y: int, terrain: TerrainType, elevation: int = 0):
        self.x = x
        self.y = y
        self.terrain = terrain
        self.elevation = elevation

    def is_walkable(self) -> bool:
        return self.terrain not in (TerrainType.SEA,)

    def update(self, dt: float):
        pass

    def render(self, surface, camera, tile_size: int, world):
        base_x = self.x * tile_size
        base_y = self.y * tile_size

        height_px = self.elevation * 8

        screen_x, screen_y = camera.apply(
            base_x,
            base_y - height_px
        )

        # Top face
        top_rect = pygame.Rect(
            screen_x,
            screen_y,
            tile_size,
            tile_size
        )
        pygame.draw.rect(surface, self._get_color(), top_rect)
        pygame.draw.rect(surface, (18, 18, 18), top_rect, 1)

        # South face
        south = world.get_zone(self.x, self.y + 1)
        if south and south.elevation < self.elevation:
            drop = (self.elevation - south.elevation) * 8
            rect = pygame.Rect(
                screen_x,
                screen_y + tile_size,
                tile_size,
                drop
            )
            pygame.draw.rect(surface, self._get_shadow_color(), rect)

        # East face
        east = world.get_zone(self.x + 1, self.y)
        if east and east.elevation < self.elevation:
            drop = (self.elevation - east.elevation) * 8
            rect = pygame.Rect(
                screen_x + tile_size,
                screen_y + tile_size,
                drop,
                tile_size
            )
            pygame.draw.rect(surface, self._get_shadow_color(), rect)

    def _get_color(self):
        if self.terrain == TerrainType.FOREST:
            return (50, 160, 60)
        if self.terrain == TerrainType.DESERT:
            return (225, 195, 135)
        if self.terrain == TerrainType.ICE:
            return (200, 235, 255)
        if self.terrain == TerrainType.SEA:
            return (0, 85, 140)
        return (120, 120, 120)

    def _get_shadow_color(self):
        base = self._get_color()
        return tuple(max(0, c - 50) for c in base)
