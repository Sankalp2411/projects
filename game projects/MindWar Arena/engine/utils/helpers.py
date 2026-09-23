# engine/utils/helpers.py
from __future__ import annotations
import functools
import time
from collections.abc import Callable
from typing import Any, TypeVar
T = TypeVar("T")
def clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(value, maximum))
def lerp(start: float, end: float, t: float) -> float:
    return start + (end - start) * clamp(t, 0.0, 1.0)
def sign(value: float) -> int:
    if value > 0:
        return 1
    if value < 0:
        return -1
    return 0
def inverse_lerp(start: float, end: float, value: float) -> float:
    if abs(end - start) < 1e-10:
        return 0.0
    return clamp((value - start) / (end - start), 0.0, 1.0)
def ease_in_out_cubic(t: float) -> float:
    t = clamp(t, 0.0, 1.0)
    if t < 0.5:
        return 4.0 * t * t * t
    return 1.0 - (-2.0 * t + 2.0) ** 3 / 2.0
def ease_out_bounce(t: float) -> float:
    t = clamp(t, 0.0, 1.0)
    n1 = 7.5625
    d1 = 2.75
    if t < 1.0 / d1:
        return n1 * t * t
    if t < 2.0 / d1:
        t -= 1.5 / d1
        return n1 * t * t + 0.75
    if t < 2.5 / d1:
        t -= 2.25 / d1
        return n1 * t * t + 0.9375
    t -= 2.625 / d1
    return n1 * t * t + 0.984375
def manhattan_distance(pos_a: tuple[int, int], pos_b: tuple[int, int]) -> int:
    return abs(pos_a[0] - pos_b[0]) + abs(pos_a[1] - pos_b[1])
def chebyshev_distance(pos_a: tuple[int, int], pos_b: tuple[int, int]) -> int:
    return max(abs(pos_a[0] - pos_b[0]), abs(pos_a[1] - pos_b[1]))
def is_within_bounds(row: int,column: int,rows: int,columns: int,) -> bool:
    return 0 <= row < rows and 0 <= column < columns
def freeze_board(board: list[list[int]]) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(row) for row in board)
def unfreeze_board(frozen: tuple[tuple[int, ...], ...],) -> list[list[int]]:
    return [list(row) for row in frozen]
def timer(func: Callable[..., T]) -> Callable[..., T]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[Timer] {func.__qualname__}: {elapsed:.4f}s")
        return result
    return wrapper
class Stopwatch:
    def __init__(self) -> None:
        self._start: float | None = None
        self._elapsed: float = 0.0
    def start(self) -> None:
        self._start = time.perf_counter()
    def stop(self) -> float:
        if self._start is not None:
            self._elapsed += time.perf_counter() - self._start
            self._start = None
        return self._elapsed
    def elapsed(self) -> float:
        if self._start is not None:
            return self._elapsed + (time.perf_counter() - self._start)
        return self._elapsed
    def reset(self) -> None:
        self._start = None
        self._elapsed = 0.0