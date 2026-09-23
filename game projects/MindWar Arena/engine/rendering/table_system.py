# engine/rendering/table_system.py
from __future__ import annotations
import math
import glm
from engine.core.event_manager import get_event_manager
from engine.utils.constants import EventType, GameMode
from engine.utils.helpers import ease_in_out_cubic
class TableSystem:
    def __init__(self,game_mode: int = GameMode.HUMAN_VS_HUMAN.value,player_names: dict[int, str] | None = None,table_radius: float = 6.5,board_size: float = 7.0,board_elevation: float = 0.45,) -> None:
        self.game_mode = game_mode
        self.table_radius = table_radius
        self.board_size = board_size
        self.board_elevation = board_elevation
        if player_names is not None:
            self.player_names = dict(player_names)
        elif self.game_mode == GameMode.HUMAN_VS_AI.value:
            self.player_names = {1: "CHALLENGER", 2: "THE MASTERMIND"}
        else:
            self.player_names = {1: "PLAYER 1 (WHITE)", 2: "PLAYER 2 (BLACK)"}
        self.current_player: int = 1
        self.active_nameplate_text: str = self.player_names.get(1, "PLAYER 1")
        self.rotation_deg: float = 0.0
        self.target_rotation_deg: float = 0.0
        self.rotation_start_deg: float = 0.0
        self.rotation_duration: float = 0.85
        self.rotation_elapsed: float = 0.0
        self.is_rotating: bool = False
        self.event_manager = get_event_manager()
        self._subscribed = False
        self.subscribe_events()
    def subscribe_events(self) -> None:
        if not self._subscribed:
            self.event_manager.subscribe(EventType.ON_TURN_CHANGED, self._on_turn_changed)
            self.event_manager.subscribe(EventType.ON_GAME_RESET, self._on_game_reset)
            self._subscribed = True
    def unsubscribe_events(self) -> None:
        if self._subscribed:
            self.event_manager.unsubscribe(EventType.ON_TURN_CHANGED, self._on_turn_changed)
            self.event_manager.unsubscribe(EventType.ON_GAME_RESET, self._on_game_reset)
            self._subscribed = False
    def _on_turn_changed(self, player: int = 1, **kwargs) -> None:
        self.on_turn_changed(player)
    def _on_game_reset(self, **kwargs) -> None:
        self.reset()
    def set_game_mode(self, mode: int) -> None:
        self.game_mode = mode
        if self.game_mode == GameMode.HUMAN_VS_AI.value:
            self.player_names = {1: "CHALLENGER", 2: "THE MASTERMIND"}
            self.rotation_deg = 0.0
            self.target_rotation_deg = 0.0
            self.is_rotating = False
        self.active_nameplate_text = self.player_names.get(self.current_player, "PLAYER")
    def on_turn_changed(self, new_player: int) -> None:
        self.current_player = new_player
        self.active_nameplate_text = self.player_names.get(new_player, f"PLAYER {new_player}")
        if self.game_mode == GameMode.HUMAN_VS_AI.value:
            return
        self.rotation_start_deg = self.rotation_deg
        target = 0.0 if new_player == 1 else 180.0
        if target <= self.rotation_start_deg:
            self.target_rotation_deg = target + 360.0
        else:
            self.target_rotation_deg = target
        self.rotation_elapsed = 0.0
        self.is_rotating = True
    def reset(self) -> None:
        self.current_player = 1
        self.rotation_deg = 0.0
        self.target_rotation_deg = 0.0
        self.rotation_start_deg = 0.0
        self.rotation_elapsed = 0.0
        self.is_rotating = False
        self.active_nameplate_text = self.player_names.get(1, "PLAYER 1")
    def update(self, delta_time: float) -> None:
        if not self.is_rotating:
            return
        self.rotation_elapsed += delta_time
        t = min(1.0, self.rotation_elapsed / self.rotation_duration)
        eased_t = ease_in_out_cubic(t)
        self.rotation_deg = (self.rotation_start_deg + (self.target_rotation_deg - self.rotation_start_deg) * eased_t)
        if t >= 1.0:
            self.rotation_deg = self.target_rotation_deg % 360.0
            self.is_rotating = False
    def get_table_matrix(self) -> glm.mat4:
        mat = glm.mat4(1.0)
        return glm.rotate(mat, glm.radians(self.rotation_deg), glm.vec3(0.0, 0.0, 1.0))
    def board_to_world(self, local_x: float, local_y: float, local_z: float = 0.0) -> glm.vec3:
        rot_rad = math.radians(self.rotation_deg)
        cos_a = math.cos(rot_rad)
        sin_a = math.sin(rot_rad)
        world_x = local_x * cos_a - local_y * sin_a
        world_y = local_x * sin_a + local_y * cos_a
        world_z = local_z + self.board_elevation
        return glm.vec3(world_x, world_y, world_z)
    def world_to_board(self, world_pt: glm.vec3) -> tuple[float, float]:
        rot_rad = -math.radians(self.rotation_deg)
        cos_a = math.cos(rot_rad)
        sin_a = math.sin(rot_rad)
        local_x = world_pt.x * cos_a - world_pt.y * sin_a
        local_y = world_pt.x * sin_a + world_pt.y * cos_a
        return (local_x, local_y)
    def get_active_player_name(self) -> str:
        return self.active_nameplate_text