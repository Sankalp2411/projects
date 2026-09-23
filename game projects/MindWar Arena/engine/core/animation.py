# engine/core/animation.py
from __future__ import annotations
from dataclasses import dataclass
from engine.utils.helpers import clamp, ease_in_out_cubic, ease_out_bounce, lerp
@dataclass
class Trajectory:
    start: tuple[float, float] = (0.0, 0.0)
    end: tuple[float, float] = (0.0, 0.0)
    duration: float = 0.3
    def __post_init__(self) -> None:
        self._elapsed: float = 0.0
        self._active: bool = False
    def start_animation(self) -> None:
        self._elapsed = 0.0
        self._active = True
    def reset(self) -> None:
        self._elapsed = 0.0
        self._active = False
    def is_active(self) -> bool:
        return self._active
    def is_done(self) -> bool:
        return self._elapsed >= self.duration
    def get_progress(self) -> float:
        if self.duration <= 0:
            return 1.0
        return clamp(self._elapsed / self.duration, 0.0, 1.0)
    def advance(self, delta_time: float) -> None:
        if not self._active:
            return
        self._elapsed += delta_time
        if self._elapsed >= self.duration:
            self._elapsed = self.duration
            self._active = False
    def get_position(self, delta_time: float = 0.0) -> tuple[float, float]:
        self.advance(delta_time)
        t = ease_in_out_cubic(self.get_progress())
        x = lerp(self.start[0], self.end[0], t)
        y = lerp(self.start[1], self.end[1], t)
        return (x, y)
@dataclass
class SlideTrajectory(Trajectory):
    def get_position(self, delta_time: float = 0.0) -> tuple[float, float]:
        self.advance(delta_time)
        t = ease_in_out_cubic(self.get_progress())
        x = lerp(self.start[0], self.end[0], t)
        y = lerp(self.start[1], self.end[1], t)
        return (x, y)
@dataclass
class ArcTrajectory(Trajectory):
    arc_height: float = 50.0
    def get_position(self, delta_time: float = 0.0) -> tuple[float, float]:
        self.advance(delta_time)
        t = ease_in_out_cubic(self.get_progress())
        x = lerp(self.start[0], self.end[0], t)
        base_y = lerp(self.start[1], self.end[1], t)
        arc_offset = -4.0 * self.arc_height * t * (1.0 - t)
        y = base_y + arc_offset
        return (x, y)
@dataclass
class DropTrajectory(Trajectory):
    def get_position(self, delta_time: float = 0.0) -> tuple[float, float]:
        self.advance(delta_time)
        t = ease_out_bounce(self.get_progress())
        x = lerp(self.start[0], self.end[0], t)
        y = lerp(self.start[1], self.end[1], t)
        return (x, y)
@dataclass
class FlipTrajectory(Trajectory):
    flip_axis: str = "x"
    def get_scale(self, delta_time: float = 0.0) -> tuple[float, float]:
        self.advance(delta_time)
        t = self.get_progress()
        if t < 0.5:
            factor = 1.0 - 2.0 * t
        else:
            factor = 2.0 * t - 1.0
        if self.flip_axis == "x":
            return (factor, 1.0)
        return (1.0, factor)
    def get_position(self, delta_time: float = 0.0) -> tuple[float, float]:
        self.advance(delta_time)
        x = (self.start[0] + self.end[0]) * 0.5
        y = (self.start[1] + self.end[1]) * 0.5
        return (x, y)
@dataclass
class FadeTrajectory(Trajectory):
    fade_in: bool = True
    def get_opacity(self, delta_time: float = 0.0) -> float:
        self.advance(delta_time)
        t = ease_in_out_cubic(self.get_progress())
        if self.fade_in:
            return t
        return 1.0 - t
    def get_position(self, delta_time: float = 0.0) -> tuple[float, float]:
        self.advance(delta_time)
        return self.start
def create_trajectory(kind: str,start: tuple[float, float],end: tuple[float, float],duration: float = 0.3,**kwargs: float,) -> Trajectory:
    factories = {"slide": SlideTrajectory,"arc": ArcTrajectory,"drop": DropTrajectory,"flip": FlipTrajectory,"fade": FadeTrajectory,}
    cls = factories.get(kind.lower())
    if cls is None:
        raise ValueError(f"Unknown trajectory kind '{kind}'. Choose from: {', '.join(factories)}")
    return cls(start=start, end=end, duration=duration, **kwargs)
LinearTrajectory = SlideTrajectory