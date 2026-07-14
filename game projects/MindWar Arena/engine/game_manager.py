"""
MindWar Arena

game_manager.py

Central game manager.

Responsibilities
----------------
• Initialize engine systems
• Run the main game loop
• Process events
• Update engine
• Render frames
• Shutdown engine
"""

import pygame

from engine.core.window import Window
from engine.core.renderer import Renderer
from engine.core.time import TimeManager
from engine.core.input import Input
from engine.core.scene_manager import SceneManager

from engine.utils.config import Config
from engine.utils.logger import Logger
from engine.utils.asset_manager import AssetManager

from game.scenes.boot_scene import BootScene


class GameManager:

    def __init__(self):

        self.running = False

        self.window = None

        self.renderer = Renderer()

        self.time_manager = TimeManager()

        self.scene_manager = SceneManager(self)

        self.fps_limit = 60

    # ---------------------------------------------------------
    # Initialization
    # ---------------------------------------------------------

    def initialize(self):

        Logger.initialize()

        Logger.info("[GameManager] Initializing...")

        Config.load()

        title = Config.get("window", "title")
        width = Config.get("window", "width")
        height = Config.get("window", "height")

        self.fps_limit = Config.get(
            "window",
            "fps_limit",
            60,
        )

        self.window = Window(
            width=width,
            height=height,
            title=title,
        )

        self.window.create()

        self.renderer.initialize(
            width,
            height,
        )

        Input.initialize()

        AssetManager.initialize()

        self.scene_manager.change_scene(
            BootScene()
        )

        self.running = True

    # ---------------------------------------------------------
    # Events
    # ---------------------------------------------------------

    def process_events(self):

        events = pygame.event.get()

        for event in events:

            if event.type == pygame.QUIT:

                self.running = False

        Input.update(events)

    # ---------------------------------------------------------
    # Update
    # ---------------------------------------------------------

    def update(self):

        self.time_manager.update()

        self.scene_manager.update()

    # ---------------------------------------------------------
    # Render
    # ---------------------------------------------------------

    def render(self):

        self.renderer.begin_frame()

        self.scene_manager.render()

        self.renderer.end_frame()

        self.window.update()

    # ---------------------------------------------------------
    # Main Loop
    # ---------------------------------------------------------

    def run(self):

        Logger.info("[GameManager] Running...")

        while self.running:

            self.process_events()

            self.update()

            self.render()

            self.window.tick(self.fps_limit)

            fps = self.time_manager.get_fps()

            if fps > 0:

                pygame.display.set_caption(
                    f"MindWar Arena | FPS: {fps}"
                )

    # ---------------------------------------------------------
    # Shutdown
    # ---------------------------------------------------------

    def shutdown(self):

        Logger.info("[GameManager] Shutting down...")

        Logger.info(
            f"[GameManager] Runtime: "
            f"{self.time_manager.get_runtime():.2f}s"
        )

        try:

            self.renderer.shutdown()

        except Exception as exception:

            Logger.error(
                f"[GameManager] Renderer shutdown error: {exception}"
            )

        try:

            self.window.destroy()

        except Exception as exception:

            Logger.error(
                f"[GameManager] Window shutdown error: {exception}"
            )

        self.running = False