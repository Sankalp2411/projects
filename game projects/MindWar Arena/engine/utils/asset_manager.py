# engine/utils/asset_manager.py
from __future__ import annotations
from pathlib import Path
from typing import Any
import pygame
from engine.utils.logger import Logger
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
class AssetManager:
    _images: dict[str, Any] = {}
    _fonts: dict[str, Any] = {}
    @classmethod
    def initialize(cls) -> None:
        Logger.info("[AssetManager] Initialized")
    @classmethod
    def load_image(cls, asset_name: str, relative_path: str) -> None:
        if asset_name in cls._images:
            Logger.warning(f"[AssetManager] Image already loaded: {asset_name}")
            return
        path = Path(relative_path)
        if not path.is_absolute():
            path = _PROJECT_ROOT / path
        if not path.exists():
            Logger.error(f"[AssetManager] Missing image: {path}")
            return
        cls._images[asset_name] = pygame.image.load(path)
        Logger.info(f"[AssetManager] Loaded image: {asset_name}")
    @classmethod
    def get_image(cls, asset_name: str) -> Any | None:
        return cls._images.get(asset_name)
    @classmethod
    def load_font(cls, asset_name: str, relative_path: str, size: int) -> None:
        key = f"{asset_name}_{size}"
        if key in cls._fonts:
            Logger.warning(f"[AssetManager] Font already loaded: {key}")
            return
        path = Path(relative_path)
        if not path.is_absolute():
            path = _PROJECT_ROOT / path
        if not path.exists():
            Logger.error(f"[AssetManager] Missing font: {path}")
            return
        cls._fonts[key] = pygame.font.Font(path, size)
        Logger.info(f"[AssetManager] Loaded font: {key}")
    @classmethod
    def get_font(cls, asset_name: str, size: int) -> Any | None:
        key = f"{asset_name}_{size}"
        return cls._fonts.get(key)
    @classmethod
    def get_loaded_image_count(cls) -> int:
        return len(cls._images)
    @classmethod
    def get_loaded_font_count(cls) -> int:
        return len(cls._fonts)
    @classmethod
    def reset(cls) -> None:
        cls._images.clear()
        cls._fonts.clear()