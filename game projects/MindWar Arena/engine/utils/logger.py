# engine/utils/logger.py
from __future__ import annotations
import threading
from datetime import datetime
from pathlib import Path
from typing import TextIO
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
class Logger:
    _log_file_path: Path | None = None
    _log_handle: TextIO | None = None
    _min_level: int = 0
    _lock: threading.Lock = threading.Lock()
    _LEVELS = {"DEBUG": 0,"INFO": 1,"WARNING": 2,"ERROR": 3,"CRITICAL": 4,}
    @classmethod
    def initialize(cls, log_dir: str | None = None, min_level: str = "DEBUG") -> None:
        cls._min_level = cls._LEVELS.get(min_level.upper(), 0)
        if log_dir is None:
            log_path = _PROJECT_ROOT / "logs"
        else:
            log_path = Path(log_dir)
        log_path.mkdir(exist_ok=True)
        cls._log_file_path = log_path / "engine.log"
        with cls._lock:
            try:
                cls._log_handle = open(cls._log_file_path, "a", encoding="utf-8")
                cls._log_handle.write("\n" + "=" * 60 + "\n")
                cls._log_handle.flush()
            except OSError as exc:
                print(f"[Logger] Failed to open log file: {exc}")
                cls._log_handle = None
        cls.info("Logger Initialized")
    @classmethod
    def shutdown(cls) -> None:
        with cls._lock:
            if cls._log_handle is not None:
                try:
                    cls._log_handle.flush()
                    cls._log_handle.close()
                except OSError:
                    pass
                cls._log_handle = None
    @classmethod
    def _write(cls, level: str, message: str) -> None:
        level_value = cls._LEVELS.get(level, 0)
        if level_value < cls._min_level:
            return
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"{timestamp} [{level}] {message}"
        print(log_line)
        with cls._lock:
            if cls._log_handle is not None:
                try:
                    cls._log_handle.write(log_line + "\n")
                    if level_value >= cls._LEVELS["WARNING"]:
                        cls._log_handle.flush()
                except OSError:
                    pass
    @classmethod
    def info(cls, message: str) -> None:
        cls._write("INFO", message)
    @classmethod
    def warning(cls, message: str) -> None:
        cls._write("WARNING", message)
    @classmethod
    def error(cls, message: str) -> None:
        cls._write("ERROR", message)
    @classmethod
    def critical(cls, message: str) -> None:
        cls._write("CRITICAL", message)
    @classmethod
    def debug(cls, message: str) -> None:
        cls._write("DEBUG", message)
    @classmethod
    def flush(cls) -> None:
        with cls._lock:
            if cls._log_handle is not None:
                try:
                    cls._log_handle.flush()
                except OSError:
                    pass
    @classmethod
    def reset(cls) -> None:
        cls.shutdown()
        cls._log_file_path = None
        cls._min_level = 0