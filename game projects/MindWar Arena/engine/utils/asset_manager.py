from pathlib import Path
import pygame
from engine.utils.logger import Logger
class AssetManager:
    _images = {}
    _fonts = {}
    @classmethod
    def initialize(cls):
        Logger.info("[AssetManager] Initialized")
    @classmethod
    def load_image(cls,asset_name,relative_path):
        if asset_name in cls._images:
            Logger.warning(f"[AssetManager] Image already loaded: {asset_name}")
            return
        path = Path(relative_path)
        if not path.exists():
            Logger.error(f"[AssetManager] Missing image: {relative_path}")
            return
        cls._images[asset_name] = pygame.image.load(path)
        Logger.info(f"[AssetManager] Loaded image: {asset_name}")
    @classmethod
    def get_image(cls,asset_name):
        return cls._images.get(asset_name)
    @classmethod
    def load_font(cls,asset_name,relative_path,size):
        key = f"{asset_name}_{size}"
        if key in cls._fonts:
            Logger.warning(f"[AssetManager] Font already loaded: {key}")
            return
        path = Path(relative_path)
        if not path.exists():
            Logger.error(f"[AssetManager] Missing font: {relative_path}")
            return
        cls._fonts[key] = pygame.font.Font(path,size)
        Logger.info(f"[AssetManager] Loaded font: {key}")
    @classmethod
    def get_font(cls,asset_name,size):
        key = f"{asset_name}_{size}"
        return cls._fonts.get(key)
    @classmethod
    def get_loaded_image_count(cls):
        return len(cls._images)
    @classmethod
    def get_loaded_font_count(cls):
        return len(cls._fonts)