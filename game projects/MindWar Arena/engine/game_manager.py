# engine/game_manager.py
from __future__ import annotations
import pygame
from engine.core.input import Input
from engine.core.renderer import Renderer
from engine.core.scene_manager import SceneManager
from engine.core.time import TimeManager
from engine.core.window import Window
from engine.utils.asset_manager import AssetManager
from engine.utils.config import Config
from engine.utils.logger import Logger
from game.scenes.boot_scene import BootScene
class GameManager:
    def __init__(self) -> None:
        self.running: bool = False
        self.window: Window | None = None
        self.renderer: Renderer = Renderer()
        self.time_manager: TimeManager = TimeManager()
        self.scene_manager: SceneManager = SceneManager(self)
        self.fps_limit: int = 60
        self._last_caption_time: float = 0.0
    def initialize(self) -> None:
        Logger.initialize()
        Logger.info("[GameManager] Initializing...")
        Config.load()
        title = Config.get("window", "title", "MindWar Arena")
        width = Config.get("window", "width", 1280)
        height = Config.get("window", "height", 720)
        self.fps_limit = Config.get("window", "fps_limit", 60)
        self.window = Window(width=width, height=height, title=title)
        self.window.create()
        self.renderer.initialize(width, height)
        Input.initialize()
        AssetManager.initialize()
        self.scene_manager.change_scene(BootScene())
        self.running = True
    def process_events(self) -> None:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
        Input.update(events)
    def update(self) -> None:
        self.time_manager.update()
        self.scene_manager.update()
    def render(self) -> None:
        self.renderer.begin_frame()
        self.scene_manager.render()
        self.renderer.end_frame()
        self.window.update()
    def run(self) -> None:
        Logger.info("[GameManager] Running...")
        while self.running:
            self.process_events()
            self.update()
            self.render()
            self.window.tick(self.fps_limit)
            now = self.time_manager.get_runtime()
            if now - self._last_caption_time >= 0.5:
                self._last_caption_time = now
                fps = self.time_manager.get_fps()
                if fps > 0:
                    pygame.display.set_caption(f"MindWar Arena | FPS: {fps}")
    def shutdown(self) -> None:
        Logger.info("[GameManager] Shutting down...")
        Logger.info(f"[GameManager] Runtime: {self.time_manager.get_runtime():.2f}s")
        try:
            self.renderer.shutdown()
        except Exception as exception:
            Logger.error(f"[GameManager] Renderer shutdown error: {exception}")
        try:
            if self.window is not None:
                self.window.destroy()
        except Exception as exception:
            Logger.error(f"[GameManager] Window shutdown error: {exception}")
        self.running = False
        Logger.shutdown()