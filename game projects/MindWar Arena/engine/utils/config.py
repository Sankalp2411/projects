# engine/utils/config.py
from __future__ import annotations
import json
from pathlib import Path
from typing import Any
from engine.utils.logger import Logger
_PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent.parent
class Config:
    _data: dict[str, Any] = {}
    @classmethod
    def load(cls, config_path: str | None = None) -> None:
        if config_path is None:
            path = _PROJECT_ROOT / "config" / "settings.json"
        else:
            path = Path(config_path)
        try:
            with open(path, encoding="utf-8") as file:
                cls._data = json.load(file)
            Logger.info(f"[Config] Loaded from {path}")
        except FileNotFoundError:
            Logger.error(f"[Config] File not found: {path}")
            cls._data = {}
        except json.JSONDecodeError as exc:
            Logger.error(f"[Config] Invalid JSON in {path}: {exc}")
            cls._data = {}
        except OSError as exc:
            Logger.error(f"[Config] Failed to read {path}: {exc}")
            cls._data = {}
    @classmethod
    def get(cls, section: str, key: str, default: Any = None) -> Any:
        section_data = cls._data.get(section)
        if isinstance(section_data, dict):
            return section_data.get(key, default)
        return default
    @classmethod
    def reset(cls) -> None:
        cls._data = {}