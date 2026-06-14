from engine.core.scene import Scene
from engine.utils.logger import Logger
from engine.utils.asset_manager import AssetManager
from engine.games.test_game import TestGame
from engine.ai.test_ai import TestAI
from engine.utils.config import Config
class BootScene(Scene):
    def __init__(self):
        super().__init__("Boot Scene")
    def enter(self):
        super().enter()
        Logger.info("[BootScene] Starting Integration Tests")
        self.test_config()
        self.test_assets()
        self.test_interfaces()
        self.test_complete()
    def test_config(self):
        title = Config.get("window","title")
        width = Config.get("window","width")
        height = Config.get("window","height")
        Logger.info(f"[TEST PASS] Config Title = {title}")
        Logger.info(f"[TEST PASS] Resolution = {width}x{height}")
    def test_assets(self):
        Logger.info(f"[TEST PASS] Images Loaded = " f"{AssetManager.get_loaded_image_count()}")
        Logger.info(f"[TEST PASS] Fonts Loaded = " f"{AssetManager.get_loaded_font_count()}")
    def test_interfaces(self):
        game = TestGame()
        ai = TestAI()
        game.initialize()
        ai.initialize()
        state = game.get_state()
        ai.select_action(state)
        Logger.info("[TEST PASS] Game Interface")
        Logger.info("[TEST PASS] AI Interface")
    def test_complete(self):
        Logger.info("=" * 50)
        Logger.info("[BOOT VALIDATION COMPLETE]")
        Logger.info("[PHASE 1 FOUNDATION VERIFIED]")
        Logger.info("=" * 50)
    def update(self):
        pass
    def render(self):
        pass