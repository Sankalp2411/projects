#engine/core/time.py
import time
class TimeManager:
    def __init__(self):
        self.delta_time = 0.0
        self.current_time = time.perf_counter()
        self.previous_time = self.current_time
        self.fps = 0
        self.frame_count = 0
        self.fps_timer = 0.0
        self.total_runtime = 0.0
    def update(self):
        self.current_time = time.perf_counter()
        self.delta_time = (self.current_time - self.previous_time)
        self.previous_time = self.current_time
        self.total_runtime += self.delta_time
        self.frame_count += 1
        self.fps_timer += self.delta_time
        if self.fps_timer >= 1.0:
            self.fps = self.frame_count
            self.frame_count = 0
            self.fps_timer = 0.0
    def get_delta_time(self):
        return self.delta_time
    def get_fps(self):
        return self.fps
    def get_runtime(self):
        return self.total_runtime