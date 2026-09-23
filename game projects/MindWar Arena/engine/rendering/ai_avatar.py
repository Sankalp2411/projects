# engine/rendering/ai_avatar.py
from __future__ import annotations
import math
from enum import Enum, auto
from typing import Any
import glm
from engine.core.event_manager import get_event_manager
from engine.utils.constants import EventType
from engine.utils.helpers import ease_in_out_cubic
class AvatarStyle(Enum):
    PRO_SUIT_MASK = auto()
    DEVIL_THRONE = auto()
class HandState(Enum):
    IDLE_ARMREST = auto()
    REACHING = auto()
    PLACING = auto()
    RETURNING = auto()
class AIAvatarController:
    def __init__(self,style: AvatarStyle = AvatarStyle.PRO_SUIT_MASK,throne_pos: glm.vec3 | None = None,) -> None:
        self.style = style
        self.throne_pos = throne_pos if throne_pos is not None else glm.vec3(0.0, 4.8, 1.2)
        self.left_hand_pos = self.throne_pos + glm.vec3(-1.7, -1.0, -0.3)
        self.right_armrest_pos = self.throne_pos + glm.vec3(1.7, -1.0, -0.3)
        self.right_hand_pos = glm.vec3(self.right_armrest_pos)
        self.hand_state = HandState.IDLE_ARMREST
        self.target_board_pos: glm.vec3 = glm.vec3(0.0, 0.0, 0.5)
        self.animation_elapsed: float = 0.0
        self.reach_duration: float = 0.55
        self.place_duration: float = 0.20
        self.return_duration: float = 0.55
        self.is_thinking: bool = False
        self.glow_intensity: float = 0.35
        self.event_manager = get_event_manager()
        self._subscribed = False
        self.subscribe_events()
    def subscribe_events(self) -> None:
        if not self._subscribed:
            self.event_manager.subscribe(EventType.ON_AI_THINKING_START, self._on_ai_thinking_start)
            self.event_manager.subscribe(EventType.ON_AI_THINKING_END, self._on_ai_thinking_end)
            self.event_manager.subscribe(EventType.ON_MOVE_MADE, self._on_move_made)
            self._subscribed = True
    def unsubscribe_events(self) -> None:
        if self._subscribed:
            self.event_manager.unsubscribe(EventType.ON_AI_THINKING_START, self._on_ai_thinking_start)
            self.event_manager.unsubscribe(EventType.ON_AI_THINKING_END, self._on_ai_thinking_end)
            self.event_manager.unsubscribe(EventType.ON_MOVE_MADE, self._on_move_made)
            self._subscribed = False
    def set_style(self, style: AvatarStyle) -> None:
        self.style = style
    def _on_ai_thinking_start(self, **kwargs) -> None:
        self.is_thinking = True
    def _on_ai_thinking_end(self, **kwargs) -> None:
        self.is_thinking = False
    def _on_move_made(self, player: int = 2, move: Any = None, **kwargs) -> None:
        if player == 2 and move is not None:
            target_world = self._convert_move_to_world(move)
            if target_world is not None:
                self.trigger_reach_and_place(target_world)
    def _convert_move_to_world(self, move: Any) -> glm.vec3 | None:
        if isinstance(move, (tuple, list)):
            if (len(move) >= 2 and isinstance(move[0], (int, float)) and isinstance(move[1], (int, float))):
                r, c = float(move[0]), float(move[1])
                wx = (c - 3.5) * 0.7
                wy = (3.5 - r) * 0.7
                return glm.vec3(wx, wy, 0.45)
            elif len(move) == 4:
                r, c = float(move[2]), float(move[3])
                wx = (c - 3.5) * 0.7
                wy = (3.5 - r) * 0.7
                return glm.vec3(wx, wy, 0.45)
        elif isinstance(move, int):
            wx = (float(move) - 3.0) * 0.8
            return glm.vec3(wx, 0.0, 0.8)
        return glm.vec3(0.0, 0.5, 0.45)
    def trigger_reach_and_place(self, target_world_pos: glm.vec3) -> None:
        self.target_board_pos = target_world_pos
        self.hand_state = HandState.REACHING
        self.animation_elapsed = 0.0
    def update(self, delta_time: float) -> None:
        if self.is_thinking:
            self.glow_intensity = 0.6 + 0.35 * math.sin(self.animation_elapsed * 6.0)
        else:
            self.glow_intensity = max(0.3, self.glow_intensity - delta_time * 0.5)
        if self.hand_state == HandState.IDLE_ARMREST:
            self.right_hand_pos = glm.vec3(self.right_armrest_pos)
            return
        self.animation_elapsed += delta_time
        if self.hand_state == HandState.REACHING:
            t = min(1.0, self.animation_elapsed / self.reach_duration)
            eased_t = ease_in_out_cubic(t)
            arc_z = 0.45 * math.sin(t * math.pi)
            self.right_hand_pos = glm.mix(self.right_armrest_pos, self.target_board_pos, eased_t)
            self.right_hand_pos.z += arc_z
            if t >= 1.0:
                self.hand_state = HandState.PLACING
                self.animation_elapsed = 0.0
        elif self.hand_state == HandState.PLACING:
            self.right_hand_pos = glm.vec3(self.target_board_pos)
            if self.animation_elapsed >= self.place_duration:
                self.hand_state = HandState.RETURNING
                self.animation_elapsed = 0.0
        elif self.hand_state == HandState.RETURNING:
            t = min(1.0, self.animation_elapsed / self.return_duration)
            eased_t = ease_in_out_cubic(t)
            arc_z = 0.35 * math.sin(t * math.pi)
            self.right_hand_pos = glm.mix(self.target_board_pos, self.right_armrest_pos, eased_t)
            self.right_hand_pos.z += arc_z
            if t >= 1.0:
                self.hand_state = HandState.IDLE_ARMREST
                self.right_hand_pos = glm.vec3(self.right_armrest_pos)
    def get_silhouette_data(self) -> dict[str, Any]:
        return { "style": self.style.name, "throne_pos": tuple(self.throne_pos), "left_hand_pos": tuple(self.left_hand_pos), "right_hand_pos": tuple(self.right_hand_pos), "glow_intensity": self.glow_intensity, "is_thinking": self.is_thinking, "hand_state": self.hand_state.name, "rim_color": (0.85, 0.15, 0.15) if self.style == AvatarStyle.DEVIL_THRONE else (0.8, 0.85, 0.95),}