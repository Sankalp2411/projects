from world.zone import Zone
from world.terrain import TerrainType
from game.slime import Slime


class World:
    TILE_SIZE = 48

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.zones = []

        self.slime = Slime(4, 4)
        self._generate_fixed_world()

    def _generate_fixed_world(self):
        for y in range(self.height):
            for x in range(self.width):
                if y < 3:
                    terrain = TerrainType.SEA
                    elevation = -1
                elif y < 5:
                    terrain = TerrainType.DESERT
                    elevation = 0
                elif y < 8:
                    terrain = TerrainType.FOREST
                    elevation = 1
                else:
                    terrain = TerrainType.ICE
                    elevation = 2

                self.zones.append(
                    Zone(x, y, terrain, elevation)
                )

    def is_valid_position(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def get_zone(self, x: int, y: int):
        for zone in self.zones:
            if zone.x == x and zone.y == y:
                return zone
        return None

    def update(self, dt: float):
        for zone in self.zones:
            zone.update(dt)

        self.slime.update(dt, self)

    def render(self, surface, camera):
        for zone in sorted(
            self.zones,
            key=lambda z: (z.y, z.elevation)
        ):
            zone.render(surface, camera, self.TILE_SIZE, self)

        self.slime.render(surface, camera, self.TILE_SIZE)
