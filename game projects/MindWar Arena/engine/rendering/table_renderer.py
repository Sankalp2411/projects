# engine/rendering/table_renderer.py
from __future__ import annotations
import math
from typing import Any
import glm
from engine.rendering.ai_avatar import AIAvatarController, AvatarStyle
from engine.rendering.camera_25d import Camera25D
from engine.rendering.table_system import TableSystem
from engine.utils.constants import GameMode
class TableRenderer:
    def __init__(self,camera: Camera25D,primitive_renderer: Any,text_renderer: Any | None = None,) -> None:
        self.camera = camera
        self.primitive_renderer = primitive_renderer
        self.text_renderer = text_renderer
    def render_environment(self,table_system: TableSystem,ai_avatar: AIAvatarController | None = None,) -> None:
        self._render_spotlight_pool(table_system)
        if table_system.game_mode == GameMode.HUMAN_VS_AI.value and ai_avatar is not None:
            self._render_ai_avatar(ai_avatar)
        self._render_table_slab(table_system)
        self._render_board_plinth(table_system)
        self._render_nameplate(table_system)
    def _render_spotlight_pool(self, table_system: TableSystem) -> None:
        table_center_world = glm.vec3(0.0, 0.0, 0.0)
        center_screen = self.camera.world_to_screen(table_center_world)
        cx, cy = center_screen.x, center_screen.y
        if hasattr(self.primitive_renderer, "draw_filled_circle"):
            self.primitive_renderer.draw_filled_circle((cx, cy),radius=380,color=(20, 24, 35, 120),segments=64,)
            self.primitive_renderer.draw_filled_circle((cx, cy),radius=290,color=(38, 45, 62, 160),segments=64,)
            self.primitive_renderer.draw_filled_circle((cx, cy),radius=210,color=(58, 66, 88, 200),segments=64,)
    def _render_ai_avatar(self, avatar: AIAvatarController) -> None:
        data = avatar.get_silhouette_data()
        throne_pos = glm.vec3(data["throne_pos"])
        screen_throne = self.camera.world_to_screen(throne_pos)
        tx, ty = screen_throne.x, screen_throne.y
        glow = data["glow_intensity"]
        rim_r = int(data["rim_color"][0] * 255 * glow)
        rim_g = int(data["rim_color"][1] * 255 * glow)
        rim_b = int(data["rim_color"][2] * 255 * glow)
        p = self.primitive_renderer
        if not hasattr(p, "draw_filled_rectangle"):
            return
        p.draw_filled_rectangle((tx - 90, ty - 220), (180, 220), (15, 16, 22, 255))
        p.draw_rectangle((tx - 90, ty - 220), (180, 220), (rim_r // 2, rim_g // 2, rim_b // 2))
        p.draw_filled_rectangle((tx - 70, ty - 120), (140, 120), (18, 20, 28, 255))
        head_radius = 36
        head_cy = ty - 150
        if hasattr(p, "draw_filled_circle"):
            p.draw_filled_circle((tx, head_cy), head_radius, (12, 14, 20, 255), segments=32)
            p.draw_circle((tx, head_cy), head_radius, (rim_r, rim_g, rim_b), segments=32)
            if avatar.style == AvatarStyle.DEVIL_THRONE:
                p.draw_line((tx - 24, head_cy - 20), (tx - 40, head_cy - 65), (rim_r, rim_g, rim_b))
                p.draw_line((tx + 24, head_cy - 20), (tx + 40, head_cy - 65), (rim_r, rim_g, rim_b))
                eye_glow = (255, 30, 30)
                p.draw_filled_circle((tx - 12, head_cy - 4), 4, eye_glow, segments=12)
                p.draw_filled_circle((tx + 12, head_cy - 4), 4, eye_glow, segments=12)
            else:
                p.draw_line((tx - 15, head_cy + 10), (tx, head_cy + 18), (rim_r, rim_g, rim_b))
                p.draw_line((tx + 15, head_cy + 10), (tx, head_cy + 18), (rim_r, rim_g, rim_b))
                p.draw_line((tx - 16, head_cy - 4), (tx - 6, head_cy - 4), (rim_r, rim_g, rim_b))
                p.draw_line((tx + 6, head_cy - 4), (tx + 16, head_cy - 4), (rim_r, rim_g, rim_b))
        lh_world = glm.vec3(data["left_hand_pos"])
        lh_screen = self.camera.world_to_screen(lh_world)
        if hasattr(p, "draw_filled_circle"):
            p.draw_filled_circle((lh_screen.x, lh_screen.y), 14, (32, 36, 48, 255), segments=16)
            p.draw_circle((lh_screen.x, lh_screen.y), 14, (rim_r // 2, rim_g // 2, rim_b // 2), segments=16)
        rh_world = glm.vec3(data["right_hand_pos"])
        rh_screen = self.camera.world_to_screen(rh_world)
        if hasattr(p, "draw_filled_circle"):
            shoulder_screen = (tx + 55, ty - 100)
            p.draw_line(shoulder_screen, (rh_screen.x, rh_screen.y), (25, 28, 38))
            p.draw_filled_circle((rh_screen.x, rh_screen.y), 16, (40, 45, 60, 255), segments=16)
            p.draw_circle((rh_screen.x, rh_screen.y), 16, (rim_r, rim_g, rim_b), segments=16)
    def _render_table_slab(self, table_system: TableSystem) -> None:
        p = self.primitive_renderer
        if not hasattr(p, "draw_filled_circle"):
            return
        center_screen = self.camera.world_to_screen(glm.vec3(0.0, 0.0, 0.0))
        cx, cy = center_screen.x, center_screen.y
        p.draw_filled_circle((cx, cy + 18), radius=225, color=(28, 22, 18, 255), segments=64)
        p.draw_filled_circle((cx, cy), radius=225, color=(48, 36, 28, 255), segments=64)
        p.draw_circle((cx, cy), radius=225, color=(90, 72, 54, 255), segments=64)
        if table_system.is_rotating:
            rot_rad = math.radians(table_system.rotation_deg)
            nx = cx + math.cos(rot_rad) * 215
            ny = cy + math.sin(rot_rad) * 215
            p.draw_line((cx, cy), (nx, ny), (180, 140, 70))
    def _render_board_plinth(self, table_system: TableSystem) -> None:
        p = self.primitive_renderer
        if not hasattr(p, "draw_filled_rectangle"):
            return
        center_screen = self.camera.world_to_screen(glm.vec3(0.0, 0.0, table_system.board_elevation))
        cx, cy = center_screen.x, center_screen.y
        plinth_w, plinth_h = 320, 240
        x = cx - plinth_w // 2
        y = cy - plinth_h // 2
        p.draw_filled_rectangle((x, y + 14), (plinth_w, plinth_h), (22, 24, 30, 255))
        p.draw_filled_rectangle((x, y), (plinth_w, plinth_h), (34, 38, 48, 255))
        p.draw_rectangle((x, y), (plinth_w, plinth_h), (65, 75, 95, 255))
    def _render_nameplate(self, table_system: TableSystem) -> None:
        p = self.primitive_renderer
        center_screen = self.camera.world_to_screen(glm.vec3(0.0, 0.0, table_system.board_elevation))
        cx, cy = center_screen.x, center_screen.y
        plate_w, plate_h = 240, 36
        px = cx - plate_w // 2
        py = cy + 122
        if hasattr(p, "draw_filled_rectangle"):
            p.draw_filled_rectangle((px, py), (plate_w, plate_h), (18, 20, 26, 240))
            border_color = (212, 175, 55, 255)
            p.draw_rectangle((px, py), (plate_w, plate_h), border_color)
            p.draw_rectangle((px + 2, py + 2), (plate_w - 4, plate_h - 4), (160, 130, 40, 180))
        if self.text_renderer is not None and hasattr(self.text_renderer, "draw_text"):
            name = table_system.get_active_player_name()
            tx = px + 16
            ty = py + 6
            self.text_renderer.draw_text(name,(tx, ty),size=20,color=(255, 230, 140),)