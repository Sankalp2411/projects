# engine/core/coordinate_mapper.py
from __future__ import annotations
import math
from dataclasses import dataclass, field
@dataclass
class GridCoordinateMapper:
    origin: tuple[float, float] = (0.0, 0.0)
    cell_size: tuple[float, float] = (64.0, 64.0)
    iso_angle: float = 0.0
    elevation_height: float = 16.0
    board_rows: int = 8
    board_columns: int = 8
    _cos_a: float = field(init=False, repr=False)
    _sin_a: float = field(init=False, repr=False)
    def __post_init__(self) -> None:
        self._update_trig()
    def set_iso_angle(self, angle: float) -> None:
        self.iso_angle = angle
        self._update_trig()
    def _update_trig(self) -> None:
        rad = math.radians(self.iso_angle)
        self._cos_a = math.cos(rad)
        self._sin_a = math.sin(rad)
    def cell_to_screen(self,col: int,row: int,*,center: bool = True,) -> tuple[float, float]:
        cw, ch = self.cell_size
        ox, oy = self.origin
        x = ox + col * cw
        y = oy + row * ch
        if center:
            x += cw * 0.5
            y += ch * 0.5
        return (x, y)
    def screen_to_cell(self,px: float,py: float,) -> tuple[int, int] | None:
        cw, ch = self.cell_size
        ox, oy = self.origin
        col = int((px - ox) / cw) if cw > 0 else 0
        row = int((py - oy) / ch) if ch > 0 else 0
        if 0 <= col < self.board_columns and 0 <= row < self.board_rows:
            return (col, row)
        return None
    def cell_to_iso(self,col: int,row: int,elevation: float = 0.0,*,center: bool = True,) -> tuple[float, float, float]:
        sx, sy = self.cell_to_screen(col, row, center=center)
        iso_x = (sx - sy) * self._cos_a
        iso_y = (sx + sy) * self._sin_a
        iso_z = elevation * self.elevation_height
        iso_y -= iso_z
        return (iso_x, iso_y, iso_z)
    def board_to_iso(self,col: int,row: int,elevation: float = 0.0,*,center: bool = True,) -> tuple[float, float, float]:
        return self.cell_to_iso(col, row, elevation, center=center)
    def iso_to_screen(self,iso_x: float,iso_y: float,iso_z: float = 0.0,) -> tuple[float, float]:
        if abs(self._cos_a) < 1e-10 or abs(self._sin_a) < 1e-10:
            return (iso_x, iso_y + iso_z)
        sx = (iso_x / self._cos_a + (iso_y + iso_z) / self._sin_a) * 0.5
        sy = ((iso_y + iso_z) / self._sin_a - iso_x / self._cos_a) * 0.5
        return (sx, sy)
    def get_board_rect(self) -> tuple[float, float, float, float]:
        ox, oy = self.origin
        cw, ch = self.cell_size
        return (ox, oy, cw * self.board_columns, ch * self.board_rows)
    def get_cell_rect(self,col: int,row: int,) -> tuple[float, float, float, float]:
        cw, ch = self.cell_size
        ox, oy = self.origin
        return (ox + col * cw, oy + row * ch, cw, ch)
    def get_intersection_point(self,col: int,row: int,) -> tuple[float, float]:
        cw, ch = self.cell_size
        ox, oy = self.origin
        return (ox + col * cw, oy + row * ch)
CoordinateMapper = GridCoordinateMapper