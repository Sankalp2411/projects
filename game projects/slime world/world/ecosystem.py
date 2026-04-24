from enum import Enum


class EcosystemState(Enum):
    EMPTY = 0
    SEEDED = 1
    ALIVE = 2
    POLLUTED = 3
    DEAD = 4
