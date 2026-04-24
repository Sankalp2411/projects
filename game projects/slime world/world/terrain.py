from enum import Enum


class TerrainType(Enum):
    SEA = 0
    DESERT = 1
    FOREST = 2
    ICE = 3

    def is_walkable(self):
        return self != TerrainType.SEA

    def movement_cost(self):
        if self == TerrainType.DESERT:
            return 1.5
        if self == TerrainType.ICE:
            return 1.2
        return 1.0
