# engine/rendering/camera_25d.py
from __future__ import annotations
import math
import glm
class Camera25D:
    def __init__(self,width: int = 1280,height: int = 720,fov_degrees: float = 45.0,tilt_degrees: float = 42.0,distance: float = 14.0,target: glm.vec3 | None = None,) -> None:
        self.width = width
        self.height = height
        self.fov = fov_degrees
        self.tilt = tilt_degrees
        self.distance = distance
        self.target = target if target is not None else glm.vec3(0.0, 0.0, 0.0)
        self._view: glm.mat4 = glm.mat4(1.0)
        self._projection: glm.mat4 = glm.mat4(1.0)
        self._view_projection: glm.mat4 = glm.mat4(1.0)
        self.eye: glm.vec3 = glm.vec3(0.0, 0.0, 0.0)
        self.update_matrices()
    def update_matrices(self) -> None:
        tilt_rad = math.radians(self.tilt)
        eye_y = self.target.y - self.distance * math.cos(tilt_rad)
        eye_z = self.target.z + self.distance * math.sin(tilt_rad)
        eye_x = self.target.x
        self.eye = glm.vec3(eye_x, eye_y, eye_z)
        up = glm.vec3(0.0, 0.0, 1.0)
        self._view = glm.lookAt(self.eye, self.target, up)
        aspect = max(self.width, 1) / max(self.height, 1)
        self._projection = glm.perspective(
            glm.radians(self.fov),aspect,0.1,100.0,)
        self._view_projection = self._projection * self._view
    def resize(self, width: int, height: int) -> None:
        if self.width == width and self.height == height:
            return
        self.width = width
        self.height = height
        self.update_matrices()
    def set_tilt(self, tilt_degrees: float) -> None:
        new_tilt = max(10.0, min(85.0, tilt_degrees))
        if abs(self.tilt - new_tilt) < 1e-4:
            return
        self.tilt = new_tilt
        self.update_matrices()
    def set_distance(self, distance: float) -> None:
        new_dist = max(4.0, min(50.0, distance))
        if abs(self.distance - new_dist) < 1e-4:
            return
        self.distance = new_dist
        self.update_matrices()
    def set_target(self, target: glm.vec3) -> None:
        if self.target == target:
            return
        self.target = target
        self.update_matrices()
    def get_view(self) -> glm.mat4:
        return self._view
    def get_projection(self) -> glm.mat4:
        return self._projection
    def get_view_projection(self) -> glm.mat4:
        return self._view_projection
    def screen_to_world_ray(self,screen_x: float,screen_y: float,) -> tuple[glm.vec3, glm.vec3]:
        viewport = glm.vec4(0, 0, self.width, self.height)
        gl_y = self.height - screen_y
        near_pt = glm.unProject(glm.vec3(screen_x, gl_y, 0.0),self._view,self._projection,viewport,)
        far_pt = glm.unProject(glm.vec3(screen_x, gl_y, 1.0),self._view,self._projection,viewport,)
        direction = glm.normalize(far_pt - near_pt)
        return near_pt, direction
    def raycast_plane_z(self,screen_x: float,screen_y: float,plane_z: float = 0.0,) -> glm.vec3 | None:
        origin, direction = self.screen_to_world_ray(screen_x, screen_y)
        if abs(direction.z) < 1e-6:
            return None
        t = (plane_z - origin.z) / direction.z
        if t < 0:
            return None
        hit_point = origin + direction * t
        return hit_point
    def world_to_screen(self, world_pos: glm.vec3) -> glm.vec2:
        clip = self._view_projection * glm.vec4(world_pos, 1.0)
        if clip.w <= 0.0:
            return glm.vec2(-9999.0, -9999.0)
        ndc = glm.vec3(clip) / clip.w
        screen_x = (ndc.x + 1.0) * 0.5 * self.width
        screen_y = (1.0 - (ndc.y + 1.0) * 0.5) * self.height
        return glm.vec2(screen_x, screen_y)